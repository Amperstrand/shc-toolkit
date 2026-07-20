#!/usr/bin/env python3
"""Monitor a VM's reachability and post a recovery notice to a support ticket.

Usage:
    python3 scripts/subnet-probe.py --service-id 1077 --ticket-id 235 [--interval 60]

Polls the VM's primary IP on TCP port 22 every N seconds. When the connection
succeeds (VM recovered from outage), posts a reply to the specified support
ticket with the recovery timestamp and total monitored outage duration.

Runs in the foreground. For background use:
    nohup python3 scripts/subnet-probe.py --service-id 1077 --ticket-id 235 &
"""
from __future__ import annotations

import argparse
import socket
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, ".")
from shc_toolkit import SHCClient


def probe(ip: str, port: int = 22, timeout: int = 10) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.close()
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--service-id", type=int, required=True)
    ap.add_argument("--ticket-id", type=int, required=True)
    ap.add_argument("--interval", type=int, default=60)
    ap.add_argument("--port", type=int, default=22)
    args = ap.parse_args()

    c = SHCClient()
    vm = c.get_vm(args.service_id)
    hostname = vm.get("hostname", "?")
    ips = [
        i.get("ip")
        for i in vm.get("ips", [])
        if isinstance(i, dict) and i.get("ip")
    ]
    if not ips:
        print(f"VM {args.service_id} has no IPs — nothing to probe", file=sys.stderr)
        sys.exit(1)

    ip = ips[0]
    start = datetime.now(timezone.utc)
    print(f"Monitoring VM {args.service_id} ({hostname}) @ {ip}:{args.port}")
    print(f"Started: {start.isoformat()}")
    print(f"Polling every {args.interval}s. Ctrl+C to stop.")
    print()

    attempt = 0
    while True:
        attempt += 1
        reachable = probe(ip, args.port)
        elapsed = (datetime.now(timezone.utc) - start).total_seconds() / 60
        status = "✅ REACHABLE" if reachable else "❌ unreachable"
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(f"  [{ts}] attempt {attempt} ({elapsed:.0f}m): {status}")

        if reachable:
            recovered = datetime.now(timezone.utc)
            outage_min = (recovered - start).total_seconds() / 60
            reply = (
                f"VM {args.service_id} ({hostname}) @ {ip} is reachable on TCP/{args.port} "
                f"as of {recovered.isoformat()}. "
                f"Monitored outage duration: {outage_min:.0f} minutes "
                f"(monitoring started {start.isoformat()}, {attempt} probes). "
                f"Service appears restored. Please confirm the subnet is stable."
            )
            try:
                r = c.reply_support_ticket(args.ticket_id, message=reply)
                print(f"\n✅ Recovery detected! Posted reply to ticket #{args.ticket_id}")
                print(f"   Reply id: {r.get('reply', {}).get('id', '?')}")
            except Exception as e:
                print(f"\n✅ Recovery detected but reply failed: {e}")
                print(f"   Manual reply needed to ticket #{args.ticket_id}")
            return

        time.sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.", file=sys.stderr)
        sys.exit(0)
