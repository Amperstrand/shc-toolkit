#!/usr/bin/env python3
"""Reap orphaned SHC VMs that are older than a threshold.

Cancels any VM whose hostname matches CI/test patterns AND has been
running longer than --max-age hours. Preserves VMs on a keep-list.

Usage:
    python scripts/reap_orphan_vms.py                  # dry run
    python scripts/reap_orphan_vms.py --execute        # actually cancel
    python scripts/reap_orphan_vms.py --execute --max-age 2

Designed to run as a scheduled CI job every 6 hours.
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone

KEEP_HOSTNAMES = {"europa-vpn-vps"}
CI_HOSTNAME_PATTERNS = [
    "pytest", "test", "ci-", "shc-runner-", "debug-",
    "e2e-host-", "europa-test-", "pool-host-",
    "europa-isp-", "europa-mptcp-",
]

DEFAULT_MAX_AGE_HOURS = 6


def is_ci_vm(hostname: str) -> bool:
    h = hostname.lower()
    return any(p in h for p in CI_HOSTNAME_PATTERNS)


def should_keep(hostname: str) -> bool:
    return hostname.lower() in KEEP_HOSTNAMES


def vm_age_hours(vm: dict) -> float:
    created = vm.get("date_created", "")
    if not created:
        return 0
    try:
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    except (ValueError, TypeError):
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Actually cancel VMs (default: dry run)")
    parser.add_argument("--max-age", type=float, default=DEFAULT_MAX_AGE_HOURS, help="Max age in hours (default: 6)")
    args = parser.parse_args()

    sys.path.insert(0, ".")
    from shc_toolkit.client import SHCClient, SHCError

    c = SHCClient()
    vms = c.list_vms()

    candidates = []
    for vm in vms:
        hostname = vm.get("hostname", "")
        if should_keep(hostname):
            continue
        if not is_ci_vm(hostname):
            continue
        age = vm_age_hours(vm)
        if age < args.max_age:
            continue
        candidates.append((vm["id"], hostname, age, vm.get("service_status", "?")))

    if not candidates:
        print(f"No orphaned VMs found (checked {len(vms)} VMs, max_age={args.max_age}h)")
        return 0

    print(f"Found {len(candidates)} orphaned VM(s) older than {args.max_age}h:")
    for sid, hostname, age, status in candidates:
        action = "CANCEL" if args.execute else "DRY-RUN"
        print(f"  [{action}] svc {sid} | {hostname} | {age:.1f}h old | {status}")

    if not args.execute:
        print("\n(dry run — use --execute to cancel)")
        return 0

    canceled = 0
    for sid, hostname, age, _ in candidates:
        for attempt in range(3):
            try:
                c.cancel_vm(sid, immediate=True)
                print(f"  ✅ Canceled svc {sid} ({hostname})")
                canceled += 1
                break
            except SHCError as e:
                if "locked" in str(e).lower() and attempt < 2:
                    print(f"  ⏳ svc {sid} locked, retrying in 20s...")
                    time.sleep(20)
                else:
                    print(f"  ❌ svc {sid}: {e}")
                    break

    print(f"\nCanceled {canceled}/{len(candidates)} orphaned VMs")
    return 0 if canceled == len(candidates) else 1


if __name__ == "__main__":
    raise SystemExit(main())
