#!/usr/bin/env python3
"""Firecracker pool concurrency benchmark.

Spawns N Firecracker microVMs concurrently on a single host, measures
boot-to-init time for each, reports parallel scalability.

Each μVM uses the same kernel + Alpine rootfs; boot is timed from
Firecracker process start to "Run /sbin/init as init process" in the
kernel log.

Usage (on the SHC host VM, not locally):
    sudo python3 firecracker-pool-bench.py --count 1
    sudo python3 firecracker-pool-bench.py --count 4
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


KERNEL = "/tmp/vmlinux-6.1"
ROOTFS_SRC = "/tmp/rootfs.ext4"  # template; each μVM gets a CoW copy
FC_BINARY = "/usr/local/bin/firecracker"


def spawn_one_umvm(idx: int) -> dict:
    """Spawn one μVM, return timing dict."""
    t0 = time.monotonic()
    workdir = Path(tempfile.mkdtemp(prefix=f"fc-{idx:02d}-"))
    socket = workdir / "fc.sock"
    console = workdir / "console.out"
    # Copy rootfs so each μVM has its own (no concurrent write contention)
    rootfs = workdir / "rootfs.ext4"
    shutil.copyfile(ROOTFS_SRC, rootfs)

    config = {
        "boot-source": {
            "kernel_image_path": KERNEL,
            "boot_args": "console=ttyS0 reboot=k panic=1 pci=off i8042.noaux",
        },
        "drives": [{
            "drive_id": "rootfs",
            "path_on_host": str(rootfs),
            "is_root_device": True,
            "is_read_only": False,
        }],
        "machine-config": {
            "vcpu_count": 1,
            "mem_size_mib": 256,
            "smt": False,
        },
    }
    cfg_path = workdir / "boot.json"
    cfg_path.write_text(json.dumps(config))

    try:
        with open(console, "wb") as console_f:
            proc = subprocess.Popen(
                [FC_BINARY, "--no-api", "--config-file", str(cfg_path)],
                stdout=console_f, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
            )
        # Wait for the kernel to reach "Run /sbin/init"
        # Poll the console file rather than block on pipe (parallel-friendly)
        deadline = time.monotonic() + 15
        init_seen_at = None
        last_size = 0
        while time.monotonic() < deadline:
            time.sleep(0.05)
            try:
                with open(console, "rb") as f:
                    f.seek(last_size)
                    chunk = f.read().decode(errors="replace")
                    last_size += len(chunk)
                    if "Run /sbin/init as init process" in chunk:
                        init_seen_at = time.monotonic()
                        break
            except Exception:
                pass
        # Give the μVM a moment more for any post-init output, then kill
        time.sleep(0.5)
        proc.send_signal(signal.SIGKILL)
        proc.wait(timeout=5)

        t_done = time.monotonic()
        return {
            "idx": idx,
            "boot_to_init_s": round(init_seen_at - t0, 3) if init_seen_at else None,
            "wall_s": round(t_done - t0, 3),
            "ok": init_seen_at is not None,
            "workdir": str(workdir),
        }
    except Exception as e:  # noqa: BLE001
        return {"idx": idx, "ok": False, "error": f"{type(e).__name__}: {e}",
                "wall_s": round(time.monotonic() - t0, 3)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1, help="μVMs to spawn concurrently")
    ap.add_argument("--keep", action="store_true",
                    help="Keep workdirs for inspection (default: clean up)")
    args = ap.parse_args()

    if not Path(KERNEL).exists():
        print(f"ERROR: kernel not found at {KERNEL}", file=sys.stderr); return 2
    if not Path(ROOTFS_SRC).exists():
        print(f"ERROR: rootfs not found at {ROOTFS_SRC}", file=sys.stderr); return 2

    print(f"=== Spawning {args.count} μVMs concurrently ===")
    print(f"Start: {time.strftime('%FT%TZ', time.gmtime())}")
    print(f"Kernel: {KERNEL} ({Path(KERNEL).stat().st_size // 1024 // 1024} MB)")
    print(f"Rootfs template: {ROOTFS_SRC} ({Path(ROOTFS_SRC).stat().st_size // 1024 // 1024} MB)")
    print()

    t_batch_start = time.monotonic()
    results = []
    with ThreadPoolExecutor(max_workers=args.count) as pool:
        futures = {pool.submit(spawn_one_umvm, i): i for i in range(args.count)}
        for fut in as_completed(futures):
            r = fut.result()
            results.append(r)
            status = "OK" if r["ok"] else "FAIL"
            boot_t = r.get("boot_to_init_s", "?")
            print(f"  μVM #{r['idx']:02d}: {status}  boot→init={boot_t}s  wall={r.get('wall_s','?')}s")
    t_batch_end = time.monotonic()
    batch_wall = round(t_batch_end - t_batch_start, 3)

    results.sort(key=lambda r: r["idx"])
    print()
    print(f"=== Batch summary: {args.count} μVMs in {batch_wall}s wall ===")
    boots = [r["boot_to_init_s"] for r in results if r.get("boot_to_init_s") is not None]
    if boots:
        print(f"  boot→init: min={min(boots):.3f}s  max={max(boots):.3f}s  avg={sum(boots)/len(boots):.3f}s")
    print(f"  throughput: {args.count / batch_wall:.2f} μVMs/sec")
    print(f"  per-μVM wall: {batch_wall / args.count:.3f}s")

    # Cleanup
    if not args.keep:
        for r in results:
            wd = r.get("workdir")
            if wd:
                shutil.rmtree(wd, ignore_errors=True)

    # Machine-readable summary on stdout last
    print()
    print("JSON:")
    print(json.dumps({
        "count": args.count,
        "batch_wall_s": batch_wall,
        "throughput_umvms_per_sec": round(args.count / batch_wall, 3),
        "results": results,
    }, indent=2, default=str))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
