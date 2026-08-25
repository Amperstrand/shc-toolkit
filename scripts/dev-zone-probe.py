#!/usr/bin/env python3
"""Dev zone (Cherryvale, KS) health probe.

Orders the smallest Dev VPS, polls until it reaches active+IP or times out,
then cancels. Exit 0 = zone healthy, exit 1 = zone broken (stuck pending).

Used to verify whether SHC issue #28 (Dev zone scheduler hang) is resolved.
Pairs with the NVMe (Katy, TX) zone as the known-good control.

Usage:
    python3 scripts/dev-zone-probe.py                    # default: 300s timeout
    python3 scripts/dev-zone-probe.py --timeout 120      # shorter wait
    python3 scripts/dev-zone-probe.py --template debian13-cloud  # test specific template

Requires: SHC_API_KEY env var. Costs ~$0.01-0.24 per run (prorated on cancel).
"""
from __future__ import annotations

import argparse
import os
import signal
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shc_toolkit import create_client

PKG_ID = 80
PRICING_ID = 241
ORDER_FORM_ID = 11
PACKAGE_GROUP_ID = 14
MODULE_GROUP_ID = 7


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=300, help="seconds to wait for ready (default 300)")
    parser.add_argument("--template", default="debian13-cloud", help="template to test (default debian13-cloud)")
    parser.add_argument("--package-id", type=int, default=PKG_ID, help="Dev VPS package (default 80)")
    parser.add_argument("--pricing-id", type=int, default=PRICING_ID, help="pricing tier (default 241 = daily)")
    args = parser.parse_args()

    if not os.environ.get("SHC_API_KEY"):
        print("FATAL: SHC_API_KEY env var not set", file=sys.stderr)
        return 2

    c = create_client(transport="rest")
    run_id = uuid.uuid4().hex[:8]
    hostname = f"devprobe-{run_id}"
    sid: int | None = None
    t0 = time.time()

    def _cancel(*_args):
        if sid:
            try:
                c.cancel_vm(sid, immediate=True)
                print(f"[{time.strftime('%H:%M:%S')}] CANCELLED sid={sid} (interrupt)")
            except Exception:
                pass
        sys.exit(1)

    signal.signal(signal.SIGINT, _cancel)
    signal.signal(signal.SIGTERM, _cancel)

    print(f"[{time.strftime('%H:%M:%S')}] Dev zone probe: pkg {args.package_id}, template={args.template}, timeout={args.timeout}s")

    try:
        result = c.submit_order(
            package_id=args.package_id,
            pricing_id=args.pricing_id,
            order_form_id=ORDER_FORM_ID,
            package_group_id=PACKAGE_GROUP_ID,
            module_group_id=MODULE_GROUP_ID,
            hostname=hostname,
            template=args.template,
            idempotency_key=f"devprobe-{run_id}",
            include_dev_vps_options=True,
        )
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ORDER FAILED: {type(e).__name__}: {e}")
        return 2

    sids = result.get("service_ids") or ([result["service_id"]] if result.get("service_id") else [])
    if not sids:
        print(f"[{time.strftime('%H:%M:%S')}] ORDER returned no service_id: {list(result.keys())}")
        return 2
    sid = int(sids[0])
    print(f"[{time.strftime('%H:%M:%S')}] Ordered sid={sid} ({time.time()-t0:.1f}s)")

    deadline = time.time() + args.timeout
    outcome = "TIMEOUT"
    last = ""
    while time.time() < deadline:
        try:
            vm = c.get_vm(sid)
            prov = vm.get("provisioning_state", "")
            svc = vm.get("service_status", "")
            ips = vm.get("ips", [])
            ip = ips[0]["ip"] if ips else None
            cur = f"prov={prov} svc={svc} ip={ip}"
            if cur != last:
                print(f"[{time.strftime('%H:%M:%S')}] {cur} ({time.time()-t0:.0f}s)")
                last = cur
            if prov == "ready":
                outcome = "READY"
                break
            if prov in ("failed", "error"):
                outcome = f"FAILED({prov})"
                break
            if svc == "active" and ip:
                outcome = f"ACTIVE(ip={ip}, prov={prov})"
                break
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] get_vm error: {e}")
        time.sleep(8)

    try:
        c.cancel_vm(sid, immediate=True)
        print(f"[{time.strftime('%H:%M:%S')}] CANCELLED sid={sid}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] CANCEL FAILED: {e}")

    elapsed = time.time() - t0
    if outcome == "READY" or outcome.startswith("ACTIVE"):
        print(f"\n✅ PASS — Dev zone healthy ({outcome}) in {elapsed:.0f}s")
        return 0
    print(f"\n❌ FAIL — Dev zone broken ({outcome}) after {elapsed:.0f}s")
    print("   Tracked in: https://github.com/Amperstrand/shc-toolkit/issues/28")
    return 1


if __name__ == "__main__":
    sys.exit(main())
