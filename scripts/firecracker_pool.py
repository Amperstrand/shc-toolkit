#!/usr/bin/env python3
"""Firecracker pool orchestrator.

Spawns/kills microVMs on a long-lived host VM, each running an ephemeral
GitHub Actions runner with a unique label. Designed for the pool-mode
architecture documented in docs/firecracker-pool-mode.md.

Requires (on host VM, set up once):
- Firecracker binary at /usr/local/bin/firecracker
- Linux 6.1+ kernel at /tmp/vmlinux-6.1
- Debian rootfs with actions-runner pre-baked at /tmp/runner-rootfs.ext4
- Networking initialized via /usr/local/bin/fc-net-init.sh
- /usr/local/bin/fc-tap-up.sh + fc-tap-down.sh

Usage:
    sudo python3 firecracker_pool.py spawn --name vm-001 --repo Amperstrand/tollgate-module-basic-go \\
        --token-file /tmp/reg-token --labels shc,fc,vm-001
    sudo python3 firecracker_pool.py kill --name vm-001
    sudo python3 firecracker_pool.py list
    sudo python3 firecracker_pool.py bench --count 4 --repo ... --token-file ...
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from pathlib import Path

FC_BINARY = "/usr/local/bin/firecracker"
KERNEL = "/tmp/vmlinux-6.1"
ROOTFS_TEMPLATE = "/tmp/runner-rootfs.ext4"
STATE_DIR = Path("/tmp/fc-pool-state")
STATE_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class MicroVM:
    name: str
    workdir: str
    tap: str
    pid: int | None = None
    started_at: float = 0.0
    boot_to_init_s: float | None = None
    ip: str | None = None
    error: str | None = None

    def save(self) -> None:
        (STATE_DIR / f"{self.name}.json").write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls, name: str) -> "MicroVM | None":
        f = STATE_DIR / f"{name}.json"
        if not f.exists():
            return None
        return cls(**json.loads(f.read_text()))

    def delete(self) -> None:
        (STATE_DIR / f"{self.name}.json").unlink(missing_ok=True)


def tap_up(name: str) -> str:
    # Truncate to keep TAP name under 15 chars (Linux IFNAMSIZ limit)
    tap = f"fctap-{name[:8]}"
    # Idempotent: delete any stale TAP from a previous failed spawn first
    subprocess.run(["ip", "link", "delete", tap],
                   check=False, capture_output=True)
    subprocess.run(["/usr/local/bin/fc-tap-up.sh", tap], check=True,
                   capture_output=True)
    return tap


def tap_down(tap: str) -> None:
    subprocess.run(["/usr/local/bin/fc-tap-down.sh", tap], check=False,
                   capture_output=True)


def spawn_one(
    name: str,
    repo: str,
    token: str,
    labels: str,
    *,
    vcpu: int = 2,
    mem_mib: int = 2048,
    timeout_s: int = 90,
    static_ip: str | None = None,
    poll_github: bool = False,
    github_token: str | None = None,
) -> MicroVM:
    """Spawn one μVM with runner. Returns when runner online OR timeout.

    static_ip: if set, uses Linux kernel `ip=` cmdline to configure eth0
               statically, bypassing DHCP. Format: "10.0.0.5".

    poll_github: if True, polls GitHub Actions API every 3s for the runner
                 showing up "online", and kills the μVM as soon as it does.
                 Requires github_token with runners:read on repo.
    """
    t0 = time.monotonic()
    workdir = Path(tempfile.mkdtemp(prefix=f"fc-{name}-"))
    vm = MicroVM(name=name, workdir=str(workdir), tap="", started_at=t0)

    try:
        tap = tap_up(name)
        vm.tap = tap

        rootfs = workdir / "rootfs.ext4"
        shutil.copyfile(ROOTFS_TEMPLATE, rootfs)

        if static_ip:
            ip_arg = f"ip={static_ip}::10.0.0.1:255.255.255.0:fc-vm:eth0:off:10.0.0.1"
        else:
            ip_arg = ""
        boot_args = (
            f"console=ttyS0 reboot=k panic=1 pci=off i8042.noaux "
            f"root=/dev/vda rw virtio_mmio.device=4K@0xd0000000:5 "
            f"{ip_arg} "
            f"FC_GITHUB_REPO={repo} FC_RUNNER_TOKEN={token} "
            f"FC_RUNNER_NAME={name} FC_RUNNER_LABELS={labels}"
        )
        config = {
            "boot-source": {
                "kernel_image_path": KERNEL,
                "boot_args": boot_args,
            },
            "drives": [{
                "drive_id": "rootfs",
                "path_on_host": str(rootfs),
                "is_root_device": True,
                "is_read_only": False,
            }],
            "machine-config": {
                "vcpu_count": vcpu,
                "mem_size_mib": mem_mib,
                "smt": False,
            },
            "network-interfaces": [{
                "iface_id": "eth0",
                "host_dev_name": tap,
            }],
        }
        cfg = workdir / "boot.json"
        cfg.write_text(json.dumps(config))

        console = workdir / "console.log"
        with open(console, "wb") as f:
            proc = subprocess.Popen(
                [FC_BINARY, "--no-api", "--config-file", str(cfg)],
                stdout=f, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
            )
        vm.pid = proc.pid

        # Phase 1: wait for kernel init
        deadline = time.monotonic() + timeout_s
        last_size = 0
        while time.monotonic() < deadline:
            time.sleep(0.1)
            try:
                with open(console, "rb") as f:
                    f.seek(last_size)
                    chunk = f.read().decode(errors="replace")
                    last_size += len(chunk)
                    if "Run /sbin/init as init process" in chunk:
                        vm.boot_to_init_s = round(time.monotonic() - t0, 3)
                        break
                    if "Kernel panic" in chunk or "not syncing" in chunk:
                        raise RuntimeError(f"kernel panic in μVM console")
            except Exception as e:
                if "panic" in str(e).lower():
                    raise

        # Phase 2: wait for runner online (via GitHub API) or deadline
        if vm.boot_to_init_s is not None:
            runner_online_at = None
            if poll_github and github_token:
                import urllib.request, urllib.error
                api_url = f"https://api.github.com/repos/{repo}/actions/runners"
                api_headers = {
                    "Authorization": f"Bearer {github_token}",
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "fc-pool-orchestrator",
                }
                while time.monotonic() < deadline:
                    try:
                        req = urllib.request.Request(api_url, headers=api_headers)
                        import ssl
                        try:
                            import certifi
                            ctx = ssl.create_default_context(cafile=certifi.where())
                        except ImportError:
                            ctx = ssl.create_default_context()
                        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                            data = json.loads(resp.read().decode())
                        for r in data.get("runners", []):
                            if r.get("name") == name and (r.get("status") or "").lower() == "online":
                                runner_online_at = time.monotonic()
                                vm.ip = static_ip or "(dhcp)"
                                break
                        if runner_online_at:
                            break
                    except Exception:
                        pass
                    time.sleep(3)
                if runner_online_at:
                    vm.boot_to_init_s = round(runner_online_at - t0, 3)
                    vm.started_at = t0
            else:
                # No GitHub polling — just wait fixed time
                remaining = max(0, deadline - time.monotonic())
                time.sleep(min(remaining, 60))

        if proc.poll() is None:
            proc.send_signal(signal.SIGKILL)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass

        vm.save()
        return vm

    except Exception as e:  # noqa: BLE001
        vm.error = f"{type(e).__name__}: {e}"
        vm.save()
        if vm.tap:
            tap_down(vm.tap)
        return vm


def kill_one(name: str) -> bool:
    """Kill a μVM by name. Returns True if killed, False if not found."""
    vm = MicroVM.load(name)
    if vm is None:
        return False
    if vm.pid:
        try:
            os.kill(vm.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if vm.tap:
        tap_down(vm.tap)
    if vm.workdir:
        shutil.rmtree(vm.workdir, ignore_errors=True)
    vm.delete()
    return True


def list_vms() -> list[MicroVM]:
    out = []
    for f in sorted(STATE_DIR.glob("*.json")):
        try:
            out.append(MicroVM(**json.loads(f.read_text())))
        except Exception:
            continue
    return out


def bench(
    count: int, repo: str, token: str, labels_prefix: str,
    *, vcpu: int = 1, mem_mib: int = 512, github_token: str | None = None,
) -> list[MicroVM]:
    """Spawn N μVMs concurrently, return all results. Uses static IPs
    10.0.0.10 + index to avoid DHCP contention."""
    t0 = time.monotonic()
    results: list[MicroVM] = []
    with ThreadPoolExecutor(max_workers=count) as pool:
        futs = {}
        for i in range(count):
            name = f"bench-{i:02d}-{int(time.time())}"
            labels = f"{labels_prefix},{name}"
            static_ip = f"10.0.0.{10 + i}"
            futs[pool.submit(spawn_one, name, repo, token, labels,
                             timeout_s=120, static_ip=static_ip,
                             vcpu=vcpu, mem_mib=mem_mib,
                             poll_github=bool(github_token),
                             github_token=github_token)] = i
        for fut in as_completed(futs):
            results.append(fut.result())
            r = results[-1]
            boot = r.boot_to_init_s if r.boot_to_init_s else "FAIL"
            print(f"  [{futs[fut]+1:2d}/{count}] {r.name}: boot={boot}s "
                  f"err={r.error or 'none'}")
    wall = time.monotonic() - t0
    boots = [r.boot_to_init_s for r in results if r.boot_to_init_s]
    print(f"\n=== {count} μVMs in {wall:.2f}s ===")
    if boots:
        print(f"  spawn-to-online: min={min(boots):.3f}  avg={sum(boots)/len(boots):.3f}  max={max(boots):.3f}")
    print(f"  throughput: {count/wall:.2f} μVMs/sec")

    for r in results:
        kill_one(r.name)

    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_spawn = sub.add_parser("spawn", help="Spawn one μVM")
    p_spawn.add_argument("--name", required=True)
    p_spawn.add_argument("--repo", required=True)
    p_spawn.add_argument("--token", required=True, help="runner registration token")
    p_spawn.add_argument("--labels", required=True)
    p_spawn.add_argument("--vcpu", type=int, default=2)
    p_spawn.add_argument("--mem-mib", type=int, default=2048)
    p_spawn.add_argument("--timeout", type=int, default=90)
    p_spawn.add_argument("--static-ip", help="e.g. 10.0.0.10; uses kernel ip= param")
    p_spawn.add_argument("--poll-github", action="store_true",
                         help="Poll GitHub for runner online; kill as soon as registered")
    p_spawn.add_argument("--github-token", help="PAT with actions:read on repo")

    p_kill = sub.add_parser("kill", help="Kill a μVM by name")
    p_kill.add_argument("--name", required=True)

    sub.add_parser("list", help="List active μVMs")

    p_bench = sub.add_parser("bench", help="Benchmark N concurrent spawns")
    p_bench.add_argument("--count", type=int, required=True)
    p_bench.add_argument("--repo", required=True)
    p_bench.add_argument("--token", required=True)
    p_bench.add_argument("--labels-prefix", default="shc,fc")
    p_bench.add_argument("--vcpu", type=int, default=1)
    p_bench.add_argument("--mem-mib", type=int, default=512)
    p_bench.add_argument("--github-token", help="if set, polls GitHub for runner online")

    args = ap.parse_args()

    if args.cmd == "spawn":
        vm = spawn_one(args.name, args.repo, args.token, args.labels,
                       vcpu=args.vcpu, mem_mib=args.mem_mib, timeout_s=args.timeout,
                       static_ip=args.static_ip,
                       poll_github=args.poll_github,
                       github_token=args.github_token)
        print(json.dumps(asdict(vm), indent=2))
        return 0 if vm.error is None else 1

    if args.cmd == "kill":
        ok = kill_one(args.name)
        print(json.dumps({"killed": ok, "name": args.name}))
        return 0 if ok else 1

    if args.cmd == "list":
        vms = list_vms()
        if not vms:
            print("(no μVMs)")
            return 0
        for vm in vms:
            print(f"  {vm.name:30s} tap={vm.tap:15s} pid={vm.pid} "
                  f"boot={vm.boot_to_init_s}s err={vm.error}")
        return 0

    if args.cmd == "bench":
        results = bench(args.count, args.repo, args.token, args.labels_prefix,
                        vcpu=args.vcpu, mem_mib=args.mem_mib,
                        github_token=args.github_token)
        ok = sum(1 for r in results if r.error is None)
        print(f"\n{ok}/{args.count} succeeded")
        return 0 if ok == args.count else 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
