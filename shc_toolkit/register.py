"""Zero-GUI SHC onboarding: register an account with nothing but a
Lightning payment.

Flow (unattended — the default; --interactive prompts for everything):
  1. generate a Nostr keypair locally (the account's identity + mailbox)
  2. email = npub…@nomail.name (nomail.name auto-creates the mailbox on
     first login; receiving is free — any SHC mail is readable with
     `shc mail` later)
  3. POST /register (anonymous) with the API's hard minimum fields —
     generated password/names, TOS accepted
  4. mint a full-scope API key over HTTP Basic (fresh accounts have no
     2FA, so no OTP is needed)
  5. link the Nostr key to the account (best-effort)
  6. top up credit via BTCPay: browser QR page (+ terminal QR fallback)
     and poll until paid — the one human act left in the flow
  7. save context '<name>' (0600) and switch to it

Referral note: /register has no referral field; attribution is
web-session based. Our affiliate link lives in the README, and a
cashu.email/nomail.name address strongly suggests tool registration.
"""

from __future__ import annotations

import json
import os
import secrets
import stat
from pathlib import Path

DEFAULT_TOPUP_USD = 1.00

CONTEXTS_DIR = Path(
    os.environ.get("SHC_CONTEXTS_DIR", "~/.config/shc/contexts")
).expanduser()


def generate_identity() -> tuple[str, str, str]:
    """(nsec, npub, email) — one keypair is account identity + mailbox."""
    from nostr_sdk import Keys

    keys = Keys.generate()
    nsec = keys.secret_key().to_bech32()
    npub = keys.public_key().to_bech32()
    return nsec, npub, f"{npub}@nomail.name"


def sign_challenge(
    nsec: str, challenge: str, *, url: str = "", method: str = "POST", kind: int = 27235
) -> dict:
    """Sign a link challenge as a NIP-98 event (kind 27235; tags u,
    method, challenge — the link-challenge response's nip98.required_tags
    names exactly these three). nomail auth accepts the same shape."""
    from nostr_sdk import EventBuilder, Keys, Kind, Tag

    keys = Keys.parse(nsec)
    tags = [Tag.parse(["challenge", challenge])]
    if url:
        tags.append(Tag.parse(["u", url]))
    tags.append(Tag.parse(["method", method.upper()]))
    event = EventBuilder(Kind(kind), challenge).tags(tags).sign_with_keys(keys)
    return json.loads(event.as_json())


def save_context(
    name: str,
    *,
    email: str,
    password: str,
    client_id,
    api_key: str,
    nsec: str,
    npub: str,
) -> Path:
    CONTEXTS_DIR.mkdir(parents=True, exist_ok=True)
    path = CONTEXTS_DIR / f"{name}.json"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(
            {
                "email": email,
                "password": password,
                "client_id": client_id,
                "api_key": api_key,
                "nsec": nsec,
                "npub": npub,
            },
            f,
            indent=2,
        )
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # umask-proof
    return path


def load_context(name: str) -> dict | None:
    path = CONTEXTS_DIR / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def register_unattended(
    client,
    *,
    topup: float = DEFAULT_TOPUP_USD,
    context: str = "default",
    browser: bool = True,
    timeout: int = 900,
    email: str | None = None,
    log=print,
) -> dict:
    """The whole wizard, zero questions. Returns the saved context dict."""
    nsec, npub, generated_email = generate_identity()
    email = email or generated_email
    password = secrets.token_urlsafe(18)
    log(f"identity: {npub[:16]}… mailbox {email[:24]}…@nomail.name")

    reg = client.register(
        email=email, password=password, first_name="shc", last_name=secrets.token_hex(4)
    )
    data = reg.get("data", reg)
    client_id = data.get("client_id")
    reg_key = (data.get("api_key") or {}).get("key", "")
    log(
        f"registered: client_id {client_id}, operate key "
        f"{'minted' if reg_key else 'NOT minted'}"
    )

    full = client.create_api_key_basic(email, password, name="shc-toolkit-full")
    api_key = (
        (full.get("data", full) or {}).get("api_key")
        or full.get("api_key")
        or full.get("key", "")
    )
    if not api_key and reg_key:
        api_key, log = (
            reg_key,
            (lambda *a, **k: log(*a, **k, note="operate-scope fallback")),
        )
    if not api_key:
        raise RuntimeError(f"no API key minted: {json.dumps(full)[:300]}")
    log("full-scope API key minted")

    try:
        chal = client.nostr_link_challenge(email, password)
        challenge = (chal.get("data", chal) or {}).get("challenge", "")
        if challenge:
            client.nostr_link(
                email,
                password,
                sign_challenge(
                    nsec,
                    challenge,
                    url=f"{client.base_url}/account/nostr/link",
                    method="POST",
                ),
            )
            log("nostr key linked")
        else:
            log(f"nostr link skipped (no challenge: {json.dumps(chal)[:120]})")
    except Exception as e:
        log(f"nostr link best-effort failed (continuing): {e}")

    creds = {
        "email": email,
        "password": password,
        "client_id": client_id,
        "api_key": api_key,
        "nsec": nsec,
        "npub": npub,
    }
    path = save_context(context, **creds)
    log(f"saved context '{context}' -> {path}")
    log(f"export SHC_API_KEY={api_key}")

    if topup > 0:
        client.session.headers["Authorization"] = f"Bearer {api_key}"
        _topup(client, topup, browser=browser, timeout=timeout, log=log)
    return {**creds, "context_path": str(path)}


_POLL_SECONDS = 10  # payment-status poll interval
_PAGE_WINDOW = 20 * 60  # QR page lifetime before re-serve/reissue
_PENDING_RETRY = 60  # wait when SHC still reports a pending top-up


def _topup(client, amount: float, *, browser: bool, timeout: int, log) -> None:
    """Serve a BTCPay top-up invoice and poll until paid.

    Live-earned contracts this encodes (2026-08-22): BTCPay invoices
    expire (~15-30 min) and SHC allows ONE pending top-up per account —
    a fresh invoice 409-conflicts until the old one lapses. The payment
    page is a single stable-URL PaymentPage whose content is UPDATED on
    each reissue (open browser tabs self-refresh), and expiry triggers
    issue-update-poll again until the overall timeout."""
    import time

    from .jit_pay import fetch_bolt11

    def issue() -> tuple:
        result = client.topup_credit(amount)
        invoice_id = result.get("invoice_id") or (result.get("data", {}) or {}).get(
            "invoice_id"
        )
        url = result.get("checkout_url") or (result.get("data", {}) or {}).get(
            "checkout_url"
        )
        if not url and invoice_id:
            pay = client._confirmed_request(
                "POST",
                f"/payment/{invoice_id}/checkout",
                json={
                    "gateway": "btcpay_server",
                    "idempotency_key": f"topup-pay-{invoice_id}",
                },
            )
            url = pay.get("checkout_url", "")
        if not url:
            raise RuntimeError(
                f"topup returned no checkout URL: {json.dumps(result)[:300]}"
            )
        return invoice_id, url

    page = None
    if browser:
        from .qr_page import PaymentPage

        page = PaymentPage()
        log(f"payment page (stable across reissues): {page.url}")
        try:
            import webbrowser

            webbrowser.open(page.url)
        except Exception:
            pass

    deadline = time.monotonic() + timeout
    invoice_id = checkout_url = None
    try:
        invoice_id, checkout_url = issue()
        log(f"top up ${amount:.2f}: {checkout_url}")
        while time.monotonic() < deadline:
            bolt11 = fetch_bolt11(checkout_url)
            if bolt11 and page:
                page.update(bolt11, amount)
            elif bolt11:
                from .jit_pay import render_qr

                render_qr(f"lightning:{bolt11}")
            expired = False
            while time.monotonic() < deadline:
                time.sleep(_POLL_SECONDS)
                st = client._get(f"/payment/{invoice_id}") if invoice_id else {}
                status = (st.get("data", st) or {}).get("status", "")
                if status in ("paid", "confirmed", "complete"):
                    log("topup received — account funded")
                    return
                if status in ("expired", "invalid"):
                    expired = True
                    break
            if time.monotonic() >= deadline or not expired:
                break
            try:
                invoice_id, checkout_url = issue()
                log(f"invoice expired — fresh one: {checkout_url}")
            except Exception as e:
                if "pending top-up" not in str(e):
                    raise
                time.sleep(_PENDING_RETRY)
        log("topup not observed as paid (check `shc balance` later)")
    finally:
        if page:
            page.close()
