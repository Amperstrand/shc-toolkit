"""Offline tests for the zero-GUI registration flow: SHCClient.register /
basic-auth / topup wrappers, nomail event signing, register.py state
machine (echo-server pattern — no network), credentials file perms, and
the ensure_api_key TTY gate.

Run: python3 -m pytest tests/test_register.py -v
"""

import pytest

pytestmark = pytest.mark.allow_network

import base64
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

import pytest

from shc_toolkit.client import SHCClient


class EchoAPI(BaseHTTPRequestHandler):
    """Records requests; replies from a scripted {path: (status, body)}."""

    calls: list[dict] = []
    script: dict[str, tuple[int, dict]] = {}
    sequences: dict[str, list[tuple[int, dict]]] = {}

    def _handle(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        rec = {
            "method": self.command,
            "path": self.path,
            "auth": self.headers.get("Authorization", ""),
            "body": body,
        }
        EchoAPI.calls.append(rec)
        key = self.path.split("?")[0]
        if key in EchoAPI.sequences:
            status, payload = EchoAPI.sequences[key].pop(0)
        else:
            status, payload = EchoAPI.script.get(key, (200, {"data": {"ok": True}}))
        out = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = _handle

    def log_message(self, *a):
        pass


@pytest.fixture()
def api():
    srv = HTTPServer(("127.0.0.1", 0), EchoAPI)
    EchoAPI.calls.clear()
    EchoAPI.script.clear()
    EchoAPI.sequences.clear()
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def _client(api):
    return SHCClient(api_key="bearer-key-for-tests", base_url=api)


# ── client wrappers ────────────────────────────────────────────────────

def test_register_sends_minimum_fields_and_no_auth(api):
    EchoAPI.script["/register"] = (200, {"data": {
        "client_id": 42,
        "api_key": {"key": "shc_live_reg"}}})
    c = _client(api)
    out = c.register(email="npub1x@nomail.name", password="pw123456",
                     first_name="shc", last_name="abcd1234")
    call = next(r for r in EchoAPI.calls if r["path"] == "/register")
    assert call["auth"] == ""  # anonymous — bearer must NOT leak
    assert set(call["body"].keys()) == {
        "email", "password", "first_name", "last_name", "tos_accepted"}
    assert call["body"]["tos_accepted"] is True
    assert out["client_id"] == 42  # _request unwraps "data"


def test_basic_auth_used_and_restored(api):
    EchoAPI.script["/account/api-keys"] = (200, {"data": {"api_key": "k2"}})
    c = _client(api)
    c.create_api_key_basic("user@x.io", "pw", name="n", scope="full")
    call = next(r for r in EchoAPI.calls if r["path"] == "/account/api-keys")
    expect = base64.b64encode(b"user@x.io:pw").decode()
    assert call["auth"] == f"Basic {expect}"
    # subsequent calls get the bearer back
    c.get_account()
    call2 = next(r for r in EchoAPI.calls if r["path"] == "/account")
    assert call2["auth"] == "Bearer bearer-key-for-tests"


def test_topup_credit_confirmed_and_idempotent(api):
    EchoAPI.script["/account/credit"] = (200, {
        "data": {"invoice_id": 7, "checkout_url": "https://btcpay/x"}})
    c = _client(api)
    out = c.topup_credit(1.0)
    call = next(r for r in EchoAPI.calls if r["path"] == "/account/credit")
    assert call["body"]["amount"] == "1.00"  # string per live-route contract
    assert len(call["body"]["idempotency_key"]) >= 16
    assert out["invoice_id"] == 7


def test_topup_reissues_on_expiry_and_finishes_on_paid(api, monkeypatch):
    """Live-earned (2026-08-22): BTCPay invoices expire and SHC allows
    one pending topup — the poll loop must reissue on 'expired' and
    return on 'paid' instead of sitting on a dead invoice."""
    from shc_toolkit import register as regmod

    monkeypatch.setattr(regmod, "_POLL_SECONDS", 0.05)
    monkeypatch.setattr("shc_toolkit.jit_pay.fetch_bolt11", lambda url: None)

    EchoAPI.sequences["/account/credit"] = [
        (200, {"data": {"invoice_id": 1, "checkout_url": "https://x/1"}}),
        (200, {"data": {"invoice_id": 2, "checkout_url": "https://x/2"}}),
    ]
    EchoAPI.sequences["/payment/1"] = [
        (200, {"data": {"status": "expired"}}),
    ]
    EchoAPI.sequences["/payment/2"] = [
        (200, {"data": {"status": "paid"}}),
    ]
    logs: list[str] = []
    c = _client(api)
    regmod._topup(c, 1.0, browser=False, timeout=10, log=logs.append)

    credits = [r for r in EchoAPI.calls if r["path"] == "/account/credit"]
    assert len(credits) == 2, "expired invoice must trigger exactly one reissue"
    assert any("fresh one" in l for l in logs)
    assert any("funded" in l for l in logs)


# ── nomail signing ─────────────────────────────────────────────────────

def test_sign_challenge_shape():
    from shc_toolkit.register import sign_challenge, generate_identity
    nsec, npub, email = generate_identity()
    assert nsec.startswith("nsec1") and npub.startswith("npub1")
    assert email == f"{npub}@nomail.name"
    ev = sign_challenge(nsec, "deadbeef" * 8)
    assert ev["kind"] == 27235
    assert ev["content"] == "deadbeef" * 8
    assert ["challenge", "deadbeef" * 8] in ev["tags"]
    assert ["method", "POST"] in ev["tags"]
    assert len(ev["sig"]) == 128 and len(ev["id"]) == 64
    assert len(ev["sig"]) == 128 and len(ev["id"]) == 64
    pytest.importorskip("nostr_sdk", reason="nostr extra not installed")
    from nostr_sdk import Keys
    assert ev["pubkey"] == Keys.parse(nsec).public_key().to_hex()


def test_nomail_login_flow(api):
    from shc_toolkit.nomail import NomailClient
    from shc_toolkit.register import generate_identity
    EchoAPI.script["/api/auth/challenge"] = (200, {"nonce": "ab" * 32})
    EchoAPI.script["/api/auth/verify"] = (200, {"pubkey": "x"})
    nsec, npub, email = generate_identity()
    box = NomailClient.login(nsec, base_url=api)
    assert box.email == f"{npub}@nomail.name"
    verify = next(r for r in EchoAPI.calls if r["path"] == "/api/auth/verify")
    ev = verify["body"]["event"]
    assert ev["tags"] == [["challenge", "ab" * 32]]
    assert ev["content"] == "ab" * 32


# ── wizard state machine ───────────────────────────────────────────────

def test_register_unattended_end_to_end(api, tmp_path, monkeypatch):
    from shc_toolkit import register as regmod

    monkeypatch.setenv("SHC_CONTEXTS_DIR", str(tmp_path / "ctx"))
    regmod.CONTEXTS_DIR = tmp_path / "ctx"

    EchoAPI.script.update({
        "/register": (200, {"data": {"client_id": 99, "api_key": None}}),
        "/account/api-keys": (200, {"data": {"api_key": "shc_live_full"}}),
        "/account/nostr/link-challenge": (200, {"data": {
            "challenge": "cd" * 32, "linked": False, "npub": None}}),
        "/account/nostr/link": (200, {"data": {"ok": True}}),
        "/account/credit": (200, {"data": {
            "invoice_id": 5, "checkout_url": "https://pay.invalid/x"}}),
    })
    logs = []
    c = _client(api)
    from shc_toolkit.register import generate_identity
    nsec, npub, email = generate_identity()
    with patch.object(regmod, "_topup"), \
         patch.object(regmod, "generate_identity",
                      side_effect=lambda: (nsec, npub, email)):
        creds = regmod.register_unattended(c, topup=1.0, context="test",
                                           log=logs.append)
    assert creds["api_key"] == "shc_live_full"
    assert creds["client_id"] == 99
    assert creds["email"] == email and creds["nsec"] == nsec
    link = next(r for r in EchoAPI.calls if r["path"] == "/account/nostr/link")
    assert link["body"]["event"]["content"] == "cd" * 32
    stored = json.loads((tmp_path / "ctx" / "test.json").read_text())
    assert stored["api_key"] == "shc_live_full"
    mode = (tmp_path / "ctx" / "test.json").stat().st_mode & 0o777
    assert mode == 0o600
    assert any("client_id 99" in l for l in logs)


def test_nostr_link_failure_is_best_effort(api, tmp_path, monkeypatch):
    from shc_toolkit import register as regmod
    monkeypatch.setenv("SHC_CONTEXTS_DIR", str(tmp_path / "ctx"))
    regmod.CONTEXTS_DIR = tmp_path / "ctx"
    EchoAPI.script.update({
        "/register": (200, {"data": {"client_id": 1, "api_key": None}}),
        "/account/api-keys": (200, {"data": {"api_key": "k"}}),
        "/account/nostr/link-challenge": (500, {"error": {"code": "boom"}}),
    })
    c = _client(api)
    with patch.object(regmod, "_topup"):
        creds = regmod.register_unattended(c, topup=0, context="t2",
                                           log=lambda *a: None)
    assert creds["api_key"] == "k"


# ── ensure_api_key TTY gate ────────────────────────────────────────────

class _NotATTY:
    def isatty(self):
        return False


def test_resolve_skips_register_when_not_tty(monkeypatch):
    from shc_toolkit import cli
    monkeypatch.delenv("SHC_API_KEY", raising=False)
    monkeypatch.delenv("SHC_PROFILE", raising=False)
    monkeypatch.setattr("sys.stdin", _NotATTY())
    # isolate from the developer's real active-profile pointer
    from shc_toolkit import profiles
    monkeypatch.setattr(profiles, "active_profile", lambda: None)
    args = type("A", (), {"api_key": None, "context": None,
                          "no_register": False})()
    assert cli._resolve_api_key(args) == ""


def test_resolve_register_gate_env(monkeypatch):
    from shc_toolkit import cli
    monkeypatch.setenv("SHC_NO_REGISTER", "1")
    monkeypatch.delenv("SHC_API_KEY", raising=False)
    monkeypatch.delenv("SHC_PROFILE", raising=False)
    monkeypatch.setattr("sys.stdin", Path("/dev/null"))
    from shc_toolkit import profiles
    monkeypatch.setattr(profiles, "active_profile", lambda: None)
    args = type("A", (), {"api_key": None, "context": None,
                          "no_register": True})()
    assert cli._resolve_api_key(args) == ""
