"""
NoDNS integration — publish DNS records via Nostr kind 11111 events.

Uses nostr-sdk (official rust-nostr Python bindings) for key generation,
event signing, and relay publishing. No hand-rolled crypto or websocket code.

Protocol: https://nodns.shop/
"""

from __future__ import annotations

import asyncio
import logging
import subprocess
import time
from dataclasses import dataclass
from typing import Any

from nostr_sdk import (
    Client,
    EventBuilder,
    Keys,
    Kind,
    NostrSigner,
    RelayUrl,
    Tag,
)

log = logging.getLogger(__name__)

RELAYS = [
    "wss://relay.damus.io",
    "wss://nos.lol",
    "wss://nostr.wine",
    "wss://relay.ngit.dev",
    "wss://relay.tollgate.me",
]

DEFAULT_ZONE = "nodns.shop"
NODNS_KIND = 11111


@dataclass
class NoDNSKeyPair:
    """Ephemeral Nostr keypair for DNS control.

    Wraps nostr_sdk.Keys with convenience methods for nodns.shop domains.
    """

    keys: Keys
    zone: str = DEFAULT_ZONE

    @classmethod
    def generate(cls, zone: str = DEFAULT_ZONE) -> NoDNSKeyPair:
        return cls(keys=Keys.generate(), zone=zone)

    @classmethod
    def from_nsec(cls, nsec: str, zone: str = DEFAULT_ZONE) -> NoDNSKeyPair:
        return cls(keys=Keys.parse(nsec), zone=zone)

    @property
    def nsec(self) -> str:
        return self.keys.secret_key().to_bech32()

    @property
    def npub(self) -> str:
        return self.keys.public_key().to_bech32()

    @property
    def pubkey_hex(self) -> str:
        return self.keys.public_key().to_hex()

    @property
    def fqdn(self) -> str:
        """Root domain: <npub>.nodns.shop"""
        return f"{self.npub}.{self.zone}"

    def subdomain(self, name: str) -> str:
        """Full subdomain: <name>.<npub>.nodns.shop"""
        return f"{name}.{self.fqdn}"

    def to_dict(self) -> dict[str, str]:
        return {
            "nsec": self.nsec,
            "npub": self.npub,
            "pubkey_hex": self.pubkey_hex,
            "fqdn": self.fqdn,
            "zone": self.zone,
        }


def build_record_tag(
    rtype: str, name: str, rdata: str, ttl: int = 300
) -> Tag:
    """Build an 11-element record tag per NoDNS spec.

    Tag format: ["record", TYPE, NAME, RDATA, "", "", "", "", "", "", TTL]
    """
    return Tag.parse(
        ["record", rtype, name, rdata, "", "", "", "", "", "", str(ttl)]
    )


async def _publish_async(
    keypair: NoDNSKeyPair,
    tags: list[Tag],
    relays: list[str],
) -> dict:
    """Async core: build event, sign, publish to relays."""
    signer = NostrSigner.keys(keypair.keys)
    client = Client(signer)

    for url in relays:
        try:
            await client.add_relay(RelayUrl.parse(url))
        except Exception as e:
            log.warning(f"Failed to add relay {url}: {e}")

    await client.connect()

    builder = EventBuilder(Kind(NODNS_KIND), "").tags(tags)
    output = await client.send_event_builder(builder)

    sent = [str(r) for r in output.success]
    failed = {str(k): str(v) for k, v in output.failed.items()}

    return {
        "event_id": output.id.to_hex(),
        "relays_sent": len(sent),
        "relays_total": len(relays),
        "sent": sent,
        "failed": failed,
    }


def publish_dns_records(
    keypair: NoDNSKeyPair,
    records: list[dict[str, Any]],
    relays: list[str] | None = None,
) -> dict:
    """Publish a kind 11111 Nostr event with DNS records.

    Args:
        keypair: Nostr keypair (controls the <npub>.nodns.shop domain).
        records: List of {type, name, value, ttl} dicts.
            name: "@" for root, or subdomain label like "www".
        relays: Override default relay list.

    Returns:
        Dict with event_id and relay results.
    """
    relays = relays or RELAYS

    tags = []
    for r in records:
        name = r.get("name", "@")
        tags.append(
            build_record_tag(
                rtype=r["type"],
                name=name,
                rdata=r["value"],
                ttl=r.get("ttl", 300),
            )
        )

    log.info(f"Publishing {len(records)} DNS records for {keypair.npub}")

    result = asyncio.run(_publish_async(keypair, tags, relays))
    result["npub"] = keypair.npub
    result["records"] = records
    return result


def verify_dns(
    fqdn: str, expected_type: str = "A", nameserver: str = "ns1.nodns.shop"
) -> dict:
    """Verify DNS resolution via dig."""
    try:
        proc = subprocess.run(
            ["dig", f"@{nameserver}", fqdn, expected_type, "+short", "+timeout=5"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        answers = [a.strip() for a in proc.stdout.strip().split("\n") if a.strip()]
        return {
            "fqdn": fqdn,
            "type": expected_type,
            "answers": answers,
            "resolved": len(answers) > 0,
        }
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return {
            "fqdn": fqdn,
            "type": expected_type,
            "answers": [],
            "resolved": False,
            "error": str(e),
        }


def provision_dns_for_vm(
    ip: str,
    subdomain: str | None = None,
    ttl: int = 300,
    wait_seconds: int = 15,
    keypair: NoDNSKeyPair | None = None,
) -> dict:
    """Full DNS provisioning: generate key, publish A record, verify.

    Args:
        ip: VM IPv4 address.
        subdomain: Optional subdomain label. None = root (@).
        ttl: DNS TTL in seconds.
        wait_seconds: Time to wait for DNS propagation (usually 3-5s).
        keypair: Existing keypair to reuse, or None to generate ephemeral.

    Returns:
        Dict with keypair info, FQDN, and verification status.
    """
    if keypair is None:
        keypair = NoDNSKeyPair.generate()

    name = subdomain if subdomain else "@"
    records = [{"type": "A", "name": name, "value": ip, "ttl": ttl}]

    log.info(f"Publishing A record: {name} -> {ip} for {keypair.npub}")

    result = publish_dns_records(keypair, records)

    fqdn = keypair.fqdn if name == "@" else keypair.subdomain(name)

    if wait_seconds > 0:
        log.info(f"Waiting {wait_seconds}s for DNS propagation...")
        time.sleep(wait_seconds)

    verification = verify_dns(fqdn, "A")

    return {
        "keypair": keypair.to_dict(),
        "fqdn": fqdn,
        "ip": ip,
        "publish_result": result,
        "dns_verification": verification,
        "success": verification.get("resolved", False),
    }


def publish_acme_challenge(
    keypair: NoDNSKeyPair,
    challenge_value: str,
    subdomain: str | None = None,
) -> dict:
    """Publish _acme-challenge TXT record for DNS-01 validation.

    Args:
        keypair: Nostr keypair controlling the domain.
        challenge_value: The ACME challenge token value from Let's Encrypt.
        subdomain: Optional subdomain. None = root domain.

    Returns:
        Publish result dict.
    """
    # ACME DNS-01 expects: _acme-challenge.<domain> TXT <token>
    # In nodns, we publish name="_acme-challenge" for root,
    # or name="_acme-challenge.www" for www subdomain
    name = "_acme-challenge" if not subdomain else f"_acme-challenge.{subdomain}"

    records = [{"type": "TXT", "name": name, "value": challenge_value, "ttl": 60}]

    log.info(f"Publishing ACME challenge TXT: {name} -> {challenge_value[:30]}...")
    return publish_dns_records(keypair, records)
