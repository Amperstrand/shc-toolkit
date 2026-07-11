from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.console_session_response_via import ConsoleSessionResponseVia
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConsoleSessionResponse")


@_attrs_define
class ConsoleSessionResponse:
    """A freshly minted, single-use noVNC console session. Open console_url in a browser before it expires.

    Attributes:
        service_id (int):
        console_url (str): Ready-to-open noVNC URL with a short-lived signed token in the fragment. Single-use.
        expires_at (datetime.datetime): ISO 8601 (UTC) instant when the session token expires.
        expires_in (int): Seconds until expiry (bridge token TTL, 5..60).
        via (ConsoleSessionResponseVia):
        ttl (int | Unset): Session ttl in seconds (v2.4.0: request a custom ttl via the optional body, clamp 5-300).
        note (str | Unset):
    """

    service_id: int
    console_url: str
    expires_at: datetime.datetime
    expires_in: int
    via: ConsoleSessionResponseVia
    ttl: int | Unset = UNSET
    note: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        console_url = self.console_url

        expires_at = self.expires_at.isoformat()

        expires_in = self.expires_in

        via = self.via.value

        ttl = self.ttl

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "console_url": console_url,
                "expires_at": expires_at,
                "expires_in": expires_in,
                "via": via,
            }
        )
        if ttl is not UNSET:
            field_dict["ttl"] = ttl
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        console_url = d.pop("console_url")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        expires_in = d.pop("expires_in")

        via = ConsoleSessionResponseVia(d.pop("via"))

        ttl = d.pop("ttl", UNSET)

        note = d.pop("note", UNSET)

        console_session_response = cls(
            service_id=service_id,
            console_url=console_url,
            expires_at=expires_at,
            expires_in=expires_in,
            via=via,
            ttl=ttl,
            note=note,
        )

        console_session_response.additional_properties = d
        return console_session_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
