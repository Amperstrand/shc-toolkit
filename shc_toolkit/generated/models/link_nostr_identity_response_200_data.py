from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.link_nostr_identity_response_200_data_status import (
    LinkNostrIdentityResponse200DataStatus,
    check_link_nostr_identity_response_200_data_status,
)

T = TypeVar("T", bound="LinkNostrIdentityResponse200Data")


@_attrs_define
class LinkNostrIdentityResponse200Data:
    status: LinkNostrIdentityResponse200DataStatus
    """ Nostr link outcome. """
    rotated: bool
    """ True when an existing linked key was replaced. """
    npub: str
    """ Linked Nostr public key in npub form. """
    nip05_name: None | str
    """ Current NIP-05 local name for the linked key, or null when absent. """

    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        rotated = self.rotated

        npub = self.npub

        nip05_name: None | str
        nip05_name = self.nip05_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "rotated": rotated,
                "npub": npub,
                "nip05_name": nip05_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = check_link_nostr_identity_response_200_data_status(d.pop("status"))

        rotated = d.pop("rotated")

        npub = d.pop("npub")

        def _parse_nip05_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        nip05_name = _parse_nip05_name(d.pop("nip05_name"))

        link_nostr_identity_response_200_data = cls(
            status=status,
            rotated=rotated,
            npub=npub,
            nip05_name=nip05_name,
        )

        return link_nostr_identity_response_200_data
