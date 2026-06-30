#!/usr/bin/env python3
"""
Hypothesis test: which payment detection method works for SHC credit topups?

Tests three methods simultaneously after the user pays a Lightning invoice:
  H1: Balance polling — GET /account/balance before/after
  H2: Idempotency replay — POST /account/credit with same key, check if status changes
  H3: Invoice listing — GET /invoices, find matching invoice by amount

Usage:
    python3 test_payment_detection.py
    (Then pay the Lightning invoice when prompted)
"""

import json
import sys
import time
import uuid
from datetime import datetime, timezone

sys.path.insert(0, ".")
from shc_toolkit.client import SHCClient


def poll_all_methods(c: SHCClient, credit_idem_key: str, amount: str,
                     balance_before: float, topup_data: dict, timeout: int = 300):
    """Poll all three detection methods simultaneously."""
    print(f"\n{'='*60}")
    print(f"  Polling 3 detection methods for up to {timeout}s...")
    print(f"{'='*60}\n")

    start = time.time()
    results = {"h1_balance": None, "h2_replay": None, "h3_invoices": None}

    while time.time() - start < timeout:
        elapsed = int(time.time() - start)

        # H1: Balance polling
        if results["h1_balance"] is None:
            try:
                balance = _get_balance(c)
                if balance > balance_before:
                    results["h1_balance"] = {
                        "detected_at": elapsed,
                        "balance_before": balance_before,
                        "balance_after": balance,
                        "delta": round(balance - balance_before, 2),
                    }
                    print(f"  [{elapsed:3d}s] H1 BALANCE: ✓ DETECTED (delta=${balance - balance_before:.2f})")
            except Exception as e:
                print(f"  [{elapsed:3d}s] H1 BALANCE: error: {e}")

        # H2: Idempotency replay
        if results["h2_replay"] is None:
            try:
                replay = _replay_topup(c, amount, credit_idem_key)
                status = replay.get("status", "?")
                if status != "checkout_required":
                    results["h2_replay"] = {
                        "detected_at": elapsed,
                        "status": status,
                        "response_keys": list(replay.keys()),
                    }
                    print(f"  [{elapsed:3d}s] H2 REPLAY:  ✓ DETECTED (status={status})")
                else:
                    pass  # Still checkout_required — not paid yet
            except Exception as e:
                err_msg = str(e)
                if "pending" in err_msg.lower() or "conflict" in err_msg.lower():
                    pass  # Expected while topup is pending
                else:
                    print(f"  [{elapsed:3d}s] H2 REPLAY:  error: {err_msg[:80]}")

        # H3: Invoice listing
        if results["h3_invoices"] is None:
            try:
                invoices = _list_invoices(c)
                matching = [inv for inv in invoices
                           if abs(float(inv.get("total", 0)) - float(amount)) < 0.01
                           or inv.get("status") in ("paid", "completed")]
                if matching:
                    inv = matching[0]
                    results["h3_invoices"] = {
                        "detected_at": elapsed,
                        "invoice_id": inv.get("id"),
                        "status": inv.get("status"),
                        "total": inv.get("total"),
                    }
                    print(f"  [{elapsed:3d}s] H3 INVOICES: ✓ DETECTED (id={inv.get('id')}, status={inv.get('status')})")
            except Exception as e:
                print(f"  [{elapsed:3d}s] H3 INVOICES: error: {e}")

        # All detected?
        if all(v is not None for v in results.values()):
            print(f"\n  All methods detected payment in {elapsed}s!")
            break

        # Still waiting
        if elapsed % 30 == 0 and elapsed > 0:
            waiting = [k for k, v in results.items() if v is None]
            print(f"  [{elapsed:3d}s] Still waiting on: {', '.join(waiting)}")

        time.sleep(3)

    return results


def _get_balance(c: SHCClient) -> float:
    data = c._get("/account/balance")
    credits = data.get("credit", [])
    for cred in credits:
        if cred.get("currency") == "USD":
            return float(cred.get("amount", 0))
    return 0.0


def _replay_topup(c: SHCClient, amount: str, idem_key: str) -> dict:
    """Replay the credit topup with the same idempotency key."""
    try:
        return c._confirmed_request("POST", "/account/credit",
                                     json={"amount": amount, "currency": "USD",
                                           "idempotency_key": idem_key})
    except Exception:
        raise


def _list_invoices(c: SHCClient) -> list:
    data = c._get("/invoices")
    return data.get("items", [])


def print_report(results: dict, topup_data: dict):
    print(f"\n{'='*60}")
    print("  HYPOTHESIS TEST REPORT")
    print(f"{'='*60}")

    for name, result in results.items():
        method_name = {"h1_balance": "Balance Polling (GET /account/balance)",
                       "h2_replay": "Idempotency Replay (POST /account/credit)",
                       "h3_invoices": "Invoice Listing (GET /invoices)"}
        print(f"\n  {method_name.get(name, name)}:")

        if result is None:
            print(f"    ✗ NOT DETECTED within timeout")
        else:
            print(f"    ✓ DETECTED at {result['detected_at']}s")
            for k, v in result.items():
                if k != "detected_at":
                    print(f"    {k}: {v}")

    working = [k for k, v in results.items() if v is not None]
    print(f"\n  Summary: {len(working)}/3 methods worked")
    if working:
        fastest = min(results[k]["detected_at"] for k in working)
        print(f"  Fastest detection: {fastest}s")
        print(f"  Recommended: {working[0]}")


def main():
    c = SHCClient()
    amount = "0.54"

    print(f"\n{'='*60}")
    print("  SHC Payment Detection Hypothesis Test")
    print(f"{'='*60}")

    # Pre-flight checks
    print("\n  Pre-flight checks...")
    try:
        balance_before = _get_balance(c)
        print(f"  Current balance: ${balance_before:.2f}")
    except Exception as e:
        print(f"  ERROR: Cannot reach SHC API: {e}")
        print("  Wait for SHC DNS to recover and try again.")
        return 1

    # Create credit topup
    credit_idem = f"hypoth-{uuid.uuid4().hex[:20]}"
    print(f"\n  Creating credit topup: ${amount} (idempotency: {credit_idem[:30]}...)")

    try:
        topup = c._confirmed_request("POST", "/account/credit",
                                      json={"amount": amount, "currency": "USD",
                                            "idempotency_key": credit_idem})
    except Exception as e:
        err = str(e)
        if "pending" in err.lower() or "conflict" in err.lower():
            print(f"\n  BLOCKED: There's a pending topup. Wait for it to expire.")
            print(f"  Error: {err[:100]}")
            return 1
        print(f"\n  ERROR creating topup: {e}")
        return 1

    bolt11 = topup.get("bolt11", "")
    checkout_url = topup.get("checkout_url", "")
    print(f"\n  Topup created!")
    print(f"  BOLT11: {bolt11[:50]}..." if bolt11 else "  BOLT11: (none)")
    print(f"  Checkout: {checkout_url}")

    # Display QR-friendly format
    print(f"\n{'='*60}")
    print(f"  ⚡ PAY THIS LIGHTNING INVOICE:")
    print(f"  {bolt11}")
    print(f"  Amount: ~{amount} USD")
    print(f"  Checkout URL: {checkout_url}")
    print(f"{'='*60}")
    print(f"\n  Pay the invoice above, then detection polling starts...")

    # Start polling
    results = poll_all_methods(c, credit_idem, amount, balance_before, topup)

    # Print report
    print_report(results, topup)

    return 0


if __name__ == "__main__":
    sys.exit(main())
