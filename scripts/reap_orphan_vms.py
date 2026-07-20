#!/usr/bin/env python3
"""Reap orphaned SHC VMs.

Two-layer detection:
1. PRIMARY: CI/test VMs without end-of-term cancellation scheduled
   (date_canceled is null). These leaked because the CI cleanup step
   didn't run. Safe to cancel immediately.

2. FALLBACK: CI/test VMs older than --max-age hours, regardless of
   cancellation status. Catches VMs where cancellation was scheduled
   but the VM is still burning credit until renewal.

Permanent VMs (europa-vpn-vps, tollgate-main-*, etc.) are never matched.

Usage:
    python scripts/reap_orphan_vms.py                       # dry run
    python scripts/reap_orphan_vms.py --execute              # cancel
    python scripts/reap_orphan_vms.py --execute --max-age 2  # >2h old
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime, timezone

KEEP_HOSTNAMES = {"europa-vpn-vps"}
KEEP_PATTERNS = ["tollgate-main-", "europa-vpn"]

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
    h = hostname.lower()
    if h in KEEP_HOSTNAMES:
        return True
    keep = KEEP_PATTERNS
    env_extra = os.environ.get("SHC_REAPER_EXTRA_KEEP_PATTERNS", "")
    if env_extra:
        keep = [*keep, *(p.strip() for p in env_extra.split(",") if p.strip())]
    return any(p in h for p in keep)


def vm_age_hours(vm: dict) -> float:
    created = vm.get("date_created", "")
    if not created:
        return 0
    try:
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    except (ValueError, TypeError):
        return 0


def has_cancel_scheduled(vm_detail: dict) -> bool:
    return vm_detail.get("date_canceled") is not None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--max-age", type=float, default=DEFAULT_MAX_AGE_HOURS)
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

        detail = c.get_vm(vm["id"])
        age = vm_age_hours(detail)
        cancel_scheduled = has_cancel_scheduled(detail)
        status = detail.get("service_status", "?")

        if not cancel_scheduled:
            reason = "NO CANCEL SCHEDULED (leaked)"
        elif age > args.max_age:
            reason = f"age={age:.1f}h > {args.max_age}h"
        else:
            continue

        candidates.append((vm["id"], hostname, age, status, reason))

    if not candidates:
        print(f"No orphaned VMs (checked {len(vms)}, keep={len(KEEP_HOSTNAMES)} permanent)")
        return 0

    print(f"Found {len(candidates)} orphaned VM(s):")
    for sid, hostname, age, status, reason in candidates:
        action = "CANCEL" if args.execute else "DRY-RUN"
        print(f"  [{action}] svc {sid} | {hostname} | {age:.1f}h | {status} | {reason}")

    if not args.execute:
        print("\n(dry run — use --execute to cancel)")
        return 0

    canceled = 0
    for sid, hostname, age, _, _ in candidates:
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

    print(f"\nCanceled {canceled}/{len(candidates)}")
    return 0 if canceled == len(candidates) else 1


if __name__ == "__main__":
    raise SystemExit(main())
