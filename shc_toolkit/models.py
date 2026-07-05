"""Typed dataclass models for SHC API responses.

These provide IDE autocomplete, type checking, and .raw dict access
for backward compatibility. The SHCClient still returns dicts; use
the from_dict() class methods to wrap them.

Example:
    >>> raw = client.list_vms()
    >>> vms = [VM.from_dict(v) for v in raw]
    >>> vms[0].hostname
    'web-server-01'
    >>> vms[0].ip
    '66.92.204.236'
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class VM:
    service_id: int
    hostname: str
    provisioning_state: str
    service_status: str
    ip: str = ""
    runtime_status: str = ""
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> VM:
        ips = d.get("ips", [])
        ip = ips[0]["ip"] if ips and isinstance(ips[0], dict) else ""
        return cls(
            service_id=int(d.get("id", 0)),
            hostname=d.get("hostname", ""),
            provisioning_state=d.get("provisioning_state", "unknown"),
            service_status=d.get("service_status", d.get("service_status", "unknown")),
            ip=ip,
            runtime_status=d.get("runtime_status", ""),
            raw=d,
        )

    @property
    def is_ready(self) -> bool:
        return self.provisioning_state == "ready"

    @property
    def ssh_target(self) -> str:
        return f"debian@{self.ip}" if self.ip else ""


@dataclass
class Balance:
    credit: float
    currency: str = "USD"
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Balance:
        credits = d.get("credit", [{}])
        entry = credits[0] if credits and isinstance(credits[0], dict) else {}
        return cls(
            credit=float(entry.get("amount", 0)),
            currency=entry.get("code", "USD"),
            raw=d,
        )


@dataclass
class CatalogPackage:
    package_id: int
    name: str
    cpu: int
    memory_mb: int
    disk_gb: int
    daily_price: float = 0.0
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> CatalogPackage:
        daily = next(
            (p for p in d.get("pricing", []) if p.get("period") == "day"),
            {},
        )
        return cls(
            package_id=int(d.get("package_id", d.get("id", 0))),
            name=d.get("name", ""),
            cpu=int(d.get("cpu", 0)),
            memory_mb=int(d.get("memory_mb", 0)),
            disk_gb=int(d.get("disk_gb", 0)),
            daily_price=float(daily.get("price", 0)),
            raw=d,
        )

    @property
    def monthly_price(self) -> float:
        return round(self.daily_price * 30, 2)


@dataclass
class SupportTicket:
    ticket_id: int
    summary: str
    status: str
    priority: str
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SupportTicket:
        return cls(
            ticket_id=int(d.get("id", 0)),
            summary=d.get("summary", ""),
            status=d.get("status", "unknown"),
            priority=d.get("priority", "medium"),
            raw=d,
        )

    @property
    def is_open(self) -> bool:
        return self.status == "open"
