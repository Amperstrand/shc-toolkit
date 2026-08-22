"""nomail.name / cashu.email client — Nostr-key email for agents.

Auth: challenge -> sign kind-1 Nostr event with tags [["challenge",
nonce]] -> verify -> __Host-session cookie. Every npub gets
npub1...@nomail.name free (receiving free; sending 100 sats — but the
test mint testnut.cashu.space auto-pays Lightning quotes, so testnet
Cashu sends are effectively free).

API reference: https://cashu.email/llms-full.txt
"""
from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

BASE_URL = "https://cashu.email"
TEST_MINT = "https://testnut.cashu.space"
SEND_COST_SATS = 100


@dataclass
class NomailClient:
    """Authenticated nomail session for one Nostr keypair."""

    npub: str
    email: str
    _client: httpx.Client

    @classmethod
    def login(cls, nsec: str, base_url: str = BASE_URL) -> "NomailClient":
        from nostr_sdk import Keys, EventBuilder, Kind, Tag

        keys = Keys.parse(nsec)
        npub = keys.public_key().to_bech32()
        with httpx.Client(base_url=base_url, timeout=30) as anon:
            nonce = anon.post("/api/auth/challenge").raise_for_status() \
                .json()["nonce"]
            event = EventBuilder(Kind(27235), nonce) \
                .tags([Tag.parse(["challenge", nonce])]) \
                .sign_with_keys(keys)
            import json as _json
            body = {"event": _json.loads(event.as_json())}
        client = httpx.Client(base_url=base_url, timeout=30)
        r = client.post("/api/auth/verify", json=body)
        r.raise_for_status()
        return cls(npub=npub, email=f"{npub}@nomail.name", _client=client)

    # ── inbox ────────────────────────────────────────────────────────
    def messages(self, limit: int = 50, offset: int = 0) -> list[dict]:
        r = self._client.get("/api/messages",
                             params={"limit": limit, "offset": offset})
        r.raise_for_status()
        return r.json().get("messages", [])

    def message(self, message_id: str) -> dict:
        r = self._client.get(f"/api/messages/{message_id}")
        r.raise_for_status()
        return r.json()

    def wait_for_message(self, match: str, *, timeout: int = 600,
                         subject: bool = True, sender: bool = True,
                         body: bool = False) -> dict | None:
        """Poll the inbox until a message matching `match` arrives.

        Matches subject/sender by default (OTP codes, receipts); pass
        body=True to also search textPreview. Returns the message dict
        or None on timeout (leaves earlier messages alone)."""
        deadline = time.monotonic() + timeout
        seen: set[str] = set()
        while time.monotonic() < deadline:
            for m in self.messages(limit=50):
                if m["id"] in seen:
                    continue
                seen.add(m["id"])
                hay = []
                if subject:
                    hay.append(m.get("subject", ""))
                if sender:
                    hay.append(m.get("fromAddr", ""))
                if body:
                    hay.append(m.get("snippet", ""))
                if match.lower() in " ".join(hay).lower():
                    return m
            time.sleep(10)
        return None

    # ── sending (Cashu or Lightning; test-mint Cashu is free) ────────
    def quote_send(self) -> dict:
        r = self._client.post("/api/send/quote")
        r.raise_for_status()
        return r.json()

    def send_with_cashu(self, to: str, subject: str, text: str,
                        cashu_token: str) -> dict:
        r = self._client.post("/api/send", json={
            "to": to, "subject": subject, "text": text,
            "cashuToken": cashu_token,
        })
        r.raise_for_status()
        return r.json()

    def addresses(self) -> list[dict]:
        r = self._client.get("/api/addresses")
        r.raise_for_status()
        return r.json().get("addresses", [])

    def close(self) -> None:
        self._client.close()
