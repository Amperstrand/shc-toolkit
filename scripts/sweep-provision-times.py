#!/usr/bin/env python3
"""Sweep SHC VM provision times across (size, template) combinations.

For each combo: orders a VM, waits until ready, captures the SHC-reported
timing, immediately cancels (with refund), and prints a comparison table.

Cost ceiling: ~$0.02 per combo (90s of usage prorated from the daily rate,
mostly refunded).

Usage:
    python3 scripts/sweep-provision-times.py
    python3 scripts/sweep-provision-times.py --size dev-1c-4gb --template alpine323-cloud
    python3 scripts/sweep-provision-times.py --repeat 2
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path

from shc_toolkit import SHCClient
from shc_toolkit.client import SHCError


DEFAULT_COMBOS: list[tuple[str, str]] = [
    ("dev-1c-4gb", "ubuntu2404-cloud"),
    ("dev-2c-8gb", "ubuntu2404-cloud"),
    ("dev-1c-4gb", "alpine323-cloud"),
]

SSH_PUB = Path.home() / ".ssh" / "id_ed25519.pub"


def sweep_one(client: SHCClient, size: str, template: str) -> dict:
    """Order one VM, wait for ready, capture timing, immediately cancel."""
    hostname = f"sweep-{uuid.uuid4().hex[:6]}"
    print(f"\n=== {size} / {template} ===", flush=True)
    t0 = time.time()

    service_id = None
    try:
        ssh_key = SSH_PUB.read_text().strip() if SSH_PUB.exists() else None
        order = client.order_vm(
            hostname=hostname,
            size=size,
            template=template,
            ssh_key=ssh_key,
            pay=True,
            check_credit=True,
        )
        service_ids = order.get("service_ids") or (
            [order["service_id"]] if order.get("service_id") else []
        )
        if not service_ids:
            return {"size": size, "template": template, "ok": False,
                    "error": f"no service_id: {order}"}
        service_id = int(service_ids[0])
        print(f"  ordered service_id={service_id}, waiting for ready...", flush=True)

        t_order = time.time()
        vm = client.wait_for_provisioning(service_id, timeout=600, interval=10)
        t_ready = time.time()
        order_to_ready = round(t_ready - t_order, 2)

        ip = vm.get("ips", [{}])[0].get("ip", "?") if vm.get("ips") else "?"
        print(f"  ready at {ip} ({order_to_ready}s order→ready)", flush=True)

        return {
            "size": size, "template": template, "ok": True,
            "service_id": service_id, "ip": ip,
            "hostname": hostname,
            "order_to_ready_s": order_to_ready,
            "total_wall_s": round(time.time() - t0, 2),
        }
    except Exception as e:  # noqa: BLE001
        return {"size": size, "template": template, "ok": False,
                "service_id": service_id,
                "error": f"{type(e).__name__}: {e}"}
    finally:
        if service_id is not None:
            try:
                client.cancel_vm(service_id, immediate=True)
                print(f"  cancelled {service_id}", flush=True)
            except SHCError as e:
                if "already" in str(e).lower() or "not found" in str(e).lower():
                    pass
                else:
                    print(f"  WARN: cancel failed: {e}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", help="single size to test (overrides defaults)")
    ap.add_argument("--template", default="ubuntu2404-cloud")
    ap.add_argument("--repeat", type=int, default=1,
                    help="run each combo N times to amortize variance")
    args = ap.parse_args()

    if args.size:
        combos = [(args.size, args.template)]
    else:
        combos = DEFAULT_COMBOS

    print(f"Sweep plan: {len(combos)} combo(s) × {args.repeat} run(s) each")
    print(f"SSH key: {SSH_PUB} ({'found' if SSH_PUB.exists() else 'NOT FOUND'})")

    client = SHCClient()
    results: list[dict] = []
    for size, template in combos:
        for run in range(args.repeat):
            r = sweep_one(client, size, template)
            r["run"] = run + 1
            results.append(r)

    print("\n" + "=" * 78)
    print(f"{'size':18s} {'template':22s} {'order→ready':>14s} {'total wall':>12s}  status")
    print("-" * 78)
    for r in results:
        if r.get("ok"):
            print(f"{r['size']:18s} {r['template']:22s} "
                  f"{r['order_to_ready_s']:>11.2f} s  "
                  f"{r['total_wall_s']:>9.2f} s  ok")
        else:
            err = (r.get('error') or '')[:40]
            print(f"{r['size']:18s} {r['template']:22s} "
                  f"{'-':>14s} {'-':>12s}  FAIL: {err}")

    print("\nJSON:")
    print(json.dumps(results, indent=2, default=str))
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
