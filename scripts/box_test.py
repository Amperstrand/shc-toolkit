#!/usr/bin/env python3
"""Overdraft-box test harness (#43 companion): squeeze testing value out of
the experiment VM without disturbing the experiment.

HARD SAFETY RULES (the experiment bills by service EXISTENCE — the guest may
be bricked freely, but the SERVICE must keep renewing):
  * NEVER: cancel, standby, resume, upgrade, term change, addons, pay —
    any billing-surface mutation is forbidden by construction (this script
    contains no calls to them).
  * Allowed: power ops (routine), reinstall (guest-destructive only),
    firewall/rdns/snapshot/cloud-init (API-side), reads of everything.

Vantage: SSH-dependent phases must run from GitHub Actions — the dev zone is
unroutable from the EU lab and has no egress (issues #39 + egress-probe
finding). API-only phases work from anywhere.

Usage:
    SHC_API_KEY=… python3 scripts/box_test.py --service-id 2540 --phase reads
    … --phase power          # restart/shutdown+start/reset matrix
    … --phase api            # firewall/rdns/snapshot/cloud-init CRUD smoke
    … --phase sweep --templates debian12-cloud,alpine323-cloud
    … --phase bench          # via SSH: openssl/dd/KVM-probe (needs GH vantage)
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shc_toolkit.client import SHCClient, SHCError

RESULTS: list[dict] = []


def record(phase: str, name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append({"phase": phase, "test": name, "ok": ok, "detail": detail[:300]})
    print(
        f"  {'PASS' if ok else 'FAIL'}  {name}"
        + (f" — {detail[:160]}" if detail else "")
    )


def ssh_run(ip: str, cmd: str, timeout: int = 60) -> tuple[int, str]:
    r = subprocess.run(
        [
            "ssh",
            "-o",
            "StrictHostKeyChecking=accept-new",
            "-o",
            "BatchMode=yes",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "ConnectTimeout=15",
            f"debian@{ip}",
            cmd,
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return r.returncode, (r.stdout + r.stderr).strip()


def banner(ip: str, timeout: float = 12.0) -> str:
    try:
        with socket.create_connection((ip, 22), timeout=timeout) as s:
            s.settimeout(6)
            return s.recv(64).decode(errors="replace").strip()
    except OSError as e:
        return f"(no banner: {type(e).__name__})"


def wait_active_ip(c: SHCClient, sid: int, timeout: int = 300) -> str | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        vm = c.get_vm(sid)
        ips = vm.get("ips", [])
        if vm.get("service_status") == "active" and ips:
            return ips[0]["ip"]
        time.sleep(10)
    return None


def phase_reads(c: SHCClient, sid: int) -> None:
    print("== phase: reads (zero-risk API surface) ==")
    for name, fn in [
        ("get_vm", lambda: c.get_vm(sid)),
        ("get_vm_summary", lambda: c.get_vm_summary(sid)),
        ("get_vm_detail", lambda: c.get_vm_detail(sid)),
        ("get_vm_metrics", lambda: c.get_vm_metrics(sid)),
        ("get_vm_bandwidth", lambda: c.get_vm_bandwidth(sid)),
        ("get_vm_activity", lambda: c.get_vm_activity(sid)),
        ("get_vm_network", lambda: c.get_vm_network(sid)),
        ("check_vm_health", lambda: c.check_vm_health(sid)),
        ("get_console_availability", lambda: c.get_console_availability(sid)),
        ("list_upgrade_options", lambda: c.list_upgrade_options(sid)),
        ("list_jobs", lambda: c.list_jobs(sid)),
        ("list_isos", lambda: c.list_isos(sid)),
    ]:
        try:
            fn()
            record("reads", name, True)
        except Exception as e:
            record("reads", name, False, f"{type(e).__name__}: {e}")


def phase_power(c: SHCClient, sid: int) -> None:
    print("== phase: power matrix (routine, ungated; billing unaffected) ==")
    steps = [
        ("restart", lambda: c.restart_vm(sid)),
        ("shutdown+start", None),  # sequenced below
        ("reset", lambda: c.reset_vm(sid)),
    ]
    for name, fn in steps:
        try:
            if name == "shutdown+start":
                c.shutdown_vm(sid)
                time.sleep(20)
                c.start_vm(sid)
            else:
                fn()
            time.sleep(15)
            vm = c.get_vm(sid)
            record("power", name, True, f"service={vm.get('service_status')}")
        except Exception as e:
            record("power", name, False, f"{type(e).__name__}: {e}")


def phase_api(c: SHCClient, sid: int) -> None:
    print("== phase: api-side CRUD smoke (routine/gated, no billing surface) ==")
    try:
        r = c.create_firewall_rule(sid, action="accept", protocol="tcp", port="22222")
        record("api", "firewall_add", bool(r))
        rules = c.get_firewall(sid)
        rules = rules.get("data", rules) if isinstance(rules, dict) else rules
        record(
            "api",
            "firewall_list",
            True,
            f"{len(rules) if isinstance(rules, list) else 'ok'} rules",
        )
        if isinstance(rules, list) and rules:
            pos = rules[0].get("position", rules[0].get("id"))
            if pos is not None:
                c.delete_firewall_rule(sid, int(pos))
                record("api", "firewall_delete", True)
    except Exception as e:
        record("api", "firewall", False, f"{type(e).__name__}: {e}")
    try:
        ip = (c.get_vm(sid).get("ips") or [{}])[0].get("ip", "")
        c.set_rdns(sid, ip, f"boxtest-{sid}.example.org")
        record("api", "rdns_set", True)
        c.list_rdns(sid)
        record("api", "rdns_list", True)
        c.clear_rdns(sid, ip)
        record("api", "rdns_clear", True)
    except Exception as e:
        record("api", "rdns", False, f"{type(e).__name__}: {e}")
    try:
        snap = c.create_snapshot(sid, name=f"boxtest-{int(time.time())}")
        record("api", "snapshot_create", bool(snap))
        c.list_snapshots(sid)
        record("api", "snapshot_list", True)
        snaps = c.list_snapshots(sid)
        snaps = snaps.get("data", snaps) if isinstance(snaps, dict) else snaps
        if snaps:
            c.delete_snapshot(sid, snaps[0].get("id") or snaps[0].get("name"))
            record("api", "snapshot_delete", True)
    except Exception as e:
        record("api", "snapshot", False, f"{type(e).__name__}: {e}")
    try:
        c.validate_vm_cloud_init(sid, cloud_init="#cloud-config\npackages: []\n")
        record("api", "cloudinit_validate", True)
        c.update_vm_cloud_init(sid, cloud_init="#cloud-config\npackages: []\n")
        record("api", "cloudinit_update", True)
    except Exception as e:
        record("api", "cloudinit", False, f"{type(e).__name__}: {e}")


def phase_sweep(
    c: SHCClient, sid: int, templates: list[str], pub_key: str | None
) -> None:
    """Reinstall sweep. Live-earned constraints (2026-09-11):
    * reinstall does NOT accept ssh_key (validation_failed: Unknown field) —
      verify via API os_template + SSH banner; key injection post-reinstall
      goes through apply_ssh_key_live (itself under test here).
    * destructive ops rate-limit hard after a burst (retry_after ~1h) —
      drip one template per pass; SHCRateLimitError aborts the phase with
      the cooldown so the caller re-dispatches later."""
    print(f"== phase: template sweep ({len(templates)} template(s), drip mode) ==")
    for tpl in templates:
        detail = ""
        try:
            c.stop_vm(sid)
            time.sleep(25)
            try:
                c.reinstall_vm(sid, template=tpl)
            finally:
                # NEVER leave the box stopped: a failed reinstall must not
                # strand it (2026-09-11: pve-ve's not_found left 2542 stopped
                # for hours; a stopped VM has no VNC, which derailed the
                # console-client live test with clean 1000-closes).
                c.start_vm(sid)
            ip = wait_active_ip(c, sid)
            api_tpl = c.get_vm(sid).get("os_template", "?")
            b = banner(ip) if ip else "(no ip)"
            ssh_ok = False
            if pub_key and ip:
                try:
                    c.apply_ssh_key_live(sid, pub_key)
                    time.sleep(10)
                    rc, _ = ssh_run(ip, "true", timeout=30)
                    ssh_ok = rc == 0
                except Exception as e:
                    detail += f" apply-live:{type(e).__name__}"
            ok = api_tpl == tpl
            detail = f"api={api_tpl} banner={b!r} ssh={ssh_ok}" + detail
            record("sweep", tpl, ok, detail)
        except SHCError as e:
            record("sweep", tpl, False, f"SHC {e.code}: {e}")
            if e.code == "rate_limited":
                wait = getattr(e, "retry_after_seconds", 0) or 3600
                print(f"  rate-limited: cooling {wait}s — re-dispatch later")
                return
        except Exception as e:
            record("sweep", tpl, False, f"{type(e).__name__}: {e}")
    # drip mode leaves the box on whatever template was last tested; the
    # caller restores debian13-cloud when the queue is done (rate limits
    # make an in-phase auto-restore unreliable)


def phase_bench(c: SHCClient, sid: int) -> None:
    print("== phase: bench via SSH (no egress needed — preinstalled tools only) ==")
    ip = wait_active_ip(c, sid)
    if not ip:
        record("bench", "reach", False, "no active+IP")
        return
    rc, out = ssh_run(
        ip,
        "nproc; grep -m1 'model name' /proc/cpuinfo; grep -i vmx /proc/cpuinfo | head -1; ls -l /dev/kvm 2>&1",
    )
    record("bench", "cpu+kvm-probe", rc == 0, out.replace("\n", " | "))
    rc, out = ssh_run(
        ip, "openssl speed -elapsed -seconds 3 aes-256-cbc 2>/dev/null | tail -2"
    )
    record("bench", "openssl-aes256", rc == 0, out.replace("\n", " | "))
    rc, out = ssh_run(
        ip,
        "dd if=/dev/zero of=/tmp/bench bs=1M count=512 oflag=direct 2>&1 | tail -1; rm -f /tmp/bench",
    )
    record("bench", "dd-disk-512M", rc == 0, out.replace("\n", " | "))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--service-id", type=int, required=True)
    p.add_argument(
        "--phase", required=True, choices=("reads", "power", "api", "sweep", "bench")
    )
    p.add_argument("--templates", default="debian12-cloud")
    p.add_argument("--ssh-key", help="path to an ephemeral pubkey for sweep/bench")
    args = p.parse_args()

    api_key = os.environ.get("SHC_API_KEY", "")
    if not api_key:
        print("ERROR: SHC_API_KEY not set", file=sys.stderr)
        return 2
    c = SHCClient(api_key=api_key)

    pub = None
    if args.ssh_key:
        pub = Path(args.ssh_key).read_text().strip()

    {
        "reads": lambda: phase_reads(c, args.service_id),
        "power": lambda: phase_power(c, args.service_id),
        "api": lambda: phase_api(c, args.service_id),
        "sweep": lambda: phase_sweep(
            c,
            args.service_id,
            [t.strip() for t in args.templates.split(",") if t.strip()],
            pub,
        ),
        "bench": lambda: phase_bench(c, args.service_id),
    }[args.phase]()

    fails = [r for r in RESULTS if not r["ok"]]
    print(f"\nbox-test: {len(RESULTS) - len(fails)}/{len(RESULTS)} passed")
    Path("/tmp/box-test-results.json").write_text(json.dumps(RESULTS, indent=2))
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
