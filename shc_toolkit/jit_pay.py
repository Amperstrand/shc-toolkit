"""
Just-in-time Lightning payment for SHC VMs.

Fetches the BOLT11 Lightning invoice from a BTCPay checkout page,
renders it as a QR code in the terminal, and polls until paid.

This enables a zero-balance workflow: order a VM, scan the QR with a
Lightning wallet, VM provisions — no stored credit to drain.
"""

from __future__ import annotations

import re
import subprocess
import time


def fetch_bolt11(checkout_url: str) -> str | None:
    """Fetch the BOLT11 Lightning invoice from a BTCPay checkout page.

    BTCPay embeds the BOLT11 in the HTML source (Vue SPA server-rendered data).
    We curl the page and regex for the lnbc/lntb prefix.
    """
    result = subprocess.run(
        ["curl", "-s", "--connect-timeout", "10", checkout_url],
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode != 0 or not result.stdout:
        return None
    matches = re.findall(r"ln(?:bc|tb|bcrt)[a-z0-9]+", result.stdout)
    return matches[0] if matches else None


def render_qr(data: str) -> bool:
    """Render data as a QR code in the terminal.

    Tries qrencode CLI first (best ANSI output), falls back to Python qrcode
    library, then plain text.
    """
    # Option 1: qrencode CLI (cleanest terminal output)
    try:
        result = subprocess.run(
            ["qrencode", "-t", "ANSIUTF8", "-o", "-", data],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout:
            print(result.stdout)
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Option 2: Python qrcode library
    try:
        import qrcode

        qr = qrcode.QRCode(border=1)
        qr.add_data(data)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
        return True
    except ImportError:
        pass

    # Option 3: plain text fallback
    print(f"\n  Lightning Invoice (copy to wallet):\n  {data}\n")
    return False


def bip21_stitch(onchain_address: str | None, bolt11: str | None) -> str | None:
    """Stitch a wallet-openable payment URI from a credit/invoice response.

    Implements the SHC operator-skills (llms-full.txt, shc-pay) table:

    - both rails  -> ``bitcoin:<addr>?lightning=<bolt11>`` (chain + Lightning)
    - on-chain    -> ``bitcoin:<addr>``
    - Lightning   -> ``lightning:<bolt11>``
    - neither     -> ``None`` (caller falls back to checkout_url)
    """
    if onchain_address and bolt11:
        return f"bitcoin:{onchain_address}?lightning={bolt11}"
    if onchain_address:
        return f"bitcoin:{onchain_address}"
    if bolt11:
        return f"lightning:{bolt11}"
    return None


def payment_uri(response_data: dict) -> str | None:
    """Best wallet-openable URI from a CreditTopupResponse-shaped dict.

    Prefers the server-provided ``payment_link`` (spec: "prefers
    lightning:…, else lightning:lnurl…, else bitcoin:…"), then falls
    back to a locally stitched BIP21 from ``onchain_address``/``bolt11``.
    """
    if not isinstance(response_data, dict):
        return None
    link = response_data.get("payment_link")
    if link:
        return link
    return bip21_stitch(
        response_data.get("onchain_address"), response_data.get("bolt11")
    )


def poll_btcpay_status(checkout_url: str, timeout: int = 900) -> bool:
    """Poll BTCPay checkout page for payment status.

    Checks every 5 seconds if the invoice page shows "paid" or "settled".
    Returns True if paid, False on timeout.
    """
    deadline = time.time() + timeout
    check_interval = 5

    while time.time() < deadline:
        result = subprocess.run(
            ["curl", "-s", "--connect-timeout", "10", checkout_url],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode == 0 and result.stdout:
            html = result.stdout.lower()
            # BTCPay shows different content when paid
            if any(
                k in html
                for k in [
                    "invoice settled",
                    "invoice paid",
                    "payment received",
                    '"status":"settled"',
                    '"status":"paid"',
                    'class="paid"',
                ]
            ):
                return True
            # Check if invoice expired
            if "invoice expired" in html or '"status":"expired"' in html:
                print("\n  Invoice expired!")
                return False

        remaining = int(deadline - time.time())
        mins, secs = divmod(max(remaining, 0), 60)
        print(
            f"\r  Waiting for payment... {mins}:{secs:02d} remaining  ",
            end="",
            flush=True,
        )
        time.sleep(check_interval)

    return False


def poll_shc_invoice(shc_client, invoice_id: int, timeout: int = 900) -> bool:
    """Poll SHC API for invoice payment status.

    More reliable than scraping BTCPay — directly checks if SHC marked
    the invoice as paid.
    """
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            inv = shc_client._get(f"/payment/{invoice_id}")
            status = str((inv.get("data", inv) or {}).get("status", "")).lower()
            if status in ("paid", "confirmed", "complete", "completed"):
                return True
            remaining = int(deadline - time.time())
            mins, secs = divmod(max(remaining, 0), 60)
            print(
                f"\r  Invoice #{invoice_id} status: {status}  "
                f"({mins}:{secs:02d} remaining)  ",
                end="",
                flush=True,
            )
        except Exception as e:
            print(f"\r  Polling error: {e}  ", end="", flush=True)
        time.sleep(5)

    return False


def jit_pay(
    shc_client,
    invoice_id: int,
    checkout_url: str,
    btcpay_invoice_id: str = "",
    timeout: int = 900,
) -> bool:
    """Full just-in-time payment flow: fetch BOLT11, show QR, wait for payment.

    Args:
        shc_client: SHCClient instance for polling invoice status.
        invoice_id: SHC invoice ID to poll.
        checkout_url: BTCPay checkout URL.
        btcpay_invoice_id: BTCPay invoice ID (for display).
        timeout: Max seconds to wait for payment (default 15 min).

    Returns:
        True if paid, False on timeout/expiry.
    """
    print(f"\n{'=' * 60}")
    print("  JUST-IN-TIME LIGHTNING PAYMENT")
    print(f"{'=' * 60}")
    print(f"  SHC Invoice:  #{invoice_id}")
    if btcpay_invoice_id:
        print(f"  BTCPay ID:    {btcpay_invoice_id}")
    print(f"  Checkout URL: {checkout_url}")
    print()

    # Step 1: Fetch BOLT11
    print("  Fetching Lightning invoice...")
    bolt11 = fetch_bolt11(checkout_url)
    if not bolt11:
        print("  ERROR: Could not extract BOLT11 from BTCPay checkout page.")
        print(f"  Pay manually: {checkout_url}")
        return False

    print(f"  BOLT11: {bolt11[:60]}...")
    print()

    # Step 2: Render QR — lightning: URI (shc-pay skill contract; wallet-openable)
    print("  Scan with your Lightning wallet:\n")
    render_qr(f"lightning:{bolt11}")
    print(f"\n  Or open in browser: {checkout_url}")
    print()

    # Step 3: Wait for payment
    print("  Waiting for payment (Ctrl+C to cancel)...")
    try:
        paid = poll_shc_invoice(shc_client, invoice_id, timeout)
    except KeyboardInterrupt:
        print("\n\n  Cancelled by user.")
        return False

    if paid:
        print("\n\n  ✓ Payment received! Invoice #{invoice_id} paid.")
        return True
    else:
        print("\n\n  ✗ Payment not received within timeout.")
        return False
