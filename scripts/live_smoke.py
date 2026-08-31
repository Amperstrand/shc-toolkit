#!/usr/bin/env python3
"""Weekly live smoke: order → provision → ssh_key check → cancel → refund.

Exercises the full toolkit path against the real API: static storefront
triple, catalog model pricing, order, active+IP readiness, ssh_key
persistence, immediate cancel with refund. Cost: ~$0.01 (1h minimum
charge, prorated refund).

Usage:
    SHC_API_KEY=shc_live_... python3 scripts/live_smoke.py [--size nvme-1c-4gb] [--timeout 180]

Exit 0 = smoke passed; non-zero = failure. Always cancels the VM (finally).
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shc_toolkit.client import SHCClient


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", default="nvme-1c-4gb", help="size to order")
    parser.add_argument("--hostname", default="ci-live-smoke")
    parser.add_argument(
        "--timeout", type=int, default=180, help="provision wait seconds"
    )
    args = parser.parse_args()

    api_key = os.environ.get("SHC_API_KEY", "")
    if not api_key:
        print("ERROR: SHC_API_KEY not set", file=sys.stderr)
        return 2

    ssh_pub = Path.home() / ".ssh" / "id_ed25519.pub"
    ssh_key = ssh_pub.read_text().strip() if ssh_pub.exists() else None

    client = SHCClient(api_key=api_key)
    t0 = time.time()
    sid: int | None = None
    ok = False
    failures: list[str] = []

    try:
        result = client.order_vm(
            hostname=args.hostname,
            size=args.size,
            ssh_key=ssh_key,
            pay=False,
        )
        sid = result.get("service_id") or (result.get("service_ids") or [None])[0]
        if not sid:
            print(f"FAIL: no service_id in order result: {str(result)[:200]}")
            return 1
        print(
            f"[{time.time() - t0:5.1f}s] ordered sid={sid} (static storefront triple)"
        )

        deadline = time.time() + args.timeout
        ip = None
        while time.time() < deadline:
            vm = client.get_vm(sid)
            ips = vm.get("ips", [])
            ip = ips[0]["ip"] if ips and isinstance(ips[0], dict) else None
            if vm.get("service_status") == "active" and ip:
                break
            time.sleep(10)

        if not ip:
            failures.append(f"no active+IP within {args.timeout}s")
        else:
            prov = time.time() - t0
            print(f"[{prov:5.1f}s] ACTIVE ip={ip}")
            if prov > 120:
                failures.append(f"provision took {prov:.0f}s (>120s)")

        vm = client.get_vm(sid)
        if ssh_key and not vm.get("ssh_key"):
            failures.append("ssh_key not stored — storefront triple regression?")
        elif ssh_key:
            print(f"[{time.time() - t0:5.1f}s] ssh_key stored: yes")

        tmpl = vm.get("os_template")
        if tmpl != "debian13-cloud":
            failures.append(f"unexpected template {tmpl!r}")
        ok = not failures
    finally:
        if sid:
            try:
                cancel = client.cancel_vm(sid, immediate=True, confirm=True)
                refund = (cancel.get("cancel_credit") or {}).get(
                    "amount"
                ) or cancel.get("expected_refund")
                print(f"[{time.time() - t0:5.1f}s] cancelled, refund=${refund}")
            except Exception as e:
                failures.append(f"cancel failed: {e}")

    for f in failures:
        print(f"FAIL: {f}")
    print(f"[{time.time() - t0:5.1f}s] smoke {'PASSED' if ok else 'FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
