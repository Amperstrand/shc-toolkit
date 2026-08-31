#!/usr/bin/env python3
"""Friendly overdraft observation probe (controlled repro for the prepaid
overdraft behavior seen on the eddy-e2e account, 2026-08-23..31).

Protocol (issue shc-toolkit#43):
  1. Fund the throwaway context (default name ``overdraft-probe``) with
     ~$0.25 via ``shc topup`` (Lightning).
  2. This probe, run on a schedule (local cron, 6h), then:
       - waits for credit >= $0.24,
       - orders exactly one ``friendly-overdraft-test`` VM (dev-1c-4gb,
         $0.24/day — cheapest daily plan),
       - snapshots credit + invoices + VM state to a JSONL log every run.
  3. Log-only: never cancels, never pays. The experiment ends when a human
     cancels the VM (after the overdraft trajectory is captured).

Usage:
    python3 scripts/overdraft-watch.py                 # snapshot (+order once funded)
    python3 scripts/overdraft-watch.py --context NAME  # other context
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shc_toolkit.client import SHCClient
from shc_toolkit.register import load_context

HOSTNAME = "friendly-overdraft-test"
PKG_ID = 80
PRICING_ID = 241
DAILY_COST = 0.24
LOG = Path.home() / ".config" / "shc" / "overdraft-watch.jsonl"


def _client(context: str) -> SHCClient:
    creds = load_context(context)
    if not creds or not creds.get("api_key"):
        raise SystemExit(f"no usable context '{context}' (shc register/topup first)")
    return SHCClient(api_key=creds["api_key"])


def _credit(c: SHCClient) -> float:
    acct = c._get("/account/credit-handling")
    for entry in acct.get("credit", acct.get("balances", [])) or []:
        try:
            return float(entry.get("amount", 0))
        except (TypeError, ValueError):
            continue
    return 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", default="overdraft-probe")
    args = parser.parse_args()

    c = _client(args.context)
    snap: dict = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    credit = _credit(c)
    snap["credit_usd"] = credit

    vms = c.list_vms()
    target = next(
        (
            v
            for v in vms
            if v.get("hostname") == HOSTNAME
            and v.get("service_status") not in ("canceled",)
        ),
        None,
    )

    if target is None and credit >= DAILY_COST:
        result = c.submit_order(
            package_id=PKG_ID,
            pricing_id=PRICING_ID,
            hostname=HOSTNAME,
            template="debian13-cloud",
            idempotency_key=f"overdraft-probe-{int(time.time())}",
            check_credit=True,
        )
        sids = result.get("service_ids") or [result.get("service_id")]
        snap["ordered"] = sids
        vms = c.list_vms()
        target = next(
            (
                v
                for v in vms
                if v.get("hostname") == HOSTNAME
                and v.get("service_status") not in ("canceled",)
            ),
            None,
        )
    elif target is None:
        snap["waiting_for_funding"] = f"credit {credit:.2f} < {DAILY_COST:.2f}"

    if target:
        snap["vm"] = {
            k: target.get(k)
            for k in (
                "id",
                "service_status",
                "provisioning_state",
                "date_created",
                "date_renews",
                "date_suspended",
            )
        }

    invoices = c.list_invoices().get("items", [])
    snap["invoices"] = [
        {
            "id": i.get("id"),
            "status": i.get("invoice_status"),
            "total": i.get("total"),
            "paid": i.get("paid"),
            "previous_due": i.get("previous_due"),
            "date_billed": i.get("date_billed"),
        }
        for i in invoices
    ]
    snap["open_invoice_total"] = sum(
        float(i.get("total", 0) or 0)
        for i in invoices
        if i.get("invoice_status") != "closed"
    )

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(snap, default=str) + "\n")
    print(json.dumps(snap, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
