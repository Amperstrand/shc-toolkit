from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.unlink_nostr_identity_response_200_data_status import (
    UnlinkNostrIdentityResponse200DataStatus,
    check_unlink_nostr_identity_response_200_data_status,
)

T = TypeVar("T", bound="UnlinkNostrIdentityResponse200Data")


@_attrs_define
class UnlinkNostrIdentityResponse200Data:
    status: UnlinkNostrIdentityResponse200DataStatus
    """ Nostr unlink outcome. """
    npub: str
    """ Nostr npub that was unlinked. """

    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        npub = self.npub

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "npub": npub,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = check_unlink_nostr_identity_response_200_data_status(d.pop("status"))

        npub = d.pop("npub")

        unlink_nostr_identity_response_200_data = cls(
            status=status,
            npub=npub,
        )

        return unlink_nostr_identity_response_200_data
