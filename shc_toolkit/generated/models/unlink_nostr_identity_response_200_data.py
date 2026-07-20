from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.unlink_nostr_identity_response_200_data_status import (
    UnlinkNostrIdentityResponse200DataStatus,
)

T = TypeVar("T", bound="UnlinkNostrIdentityResponse200Data")


@_attrs_define
class UnlinkNostrIdentityResponse200Data:
    """
    Attributes:
        status (UnlinkNostrIdentityResponse200DataStatus): Nostr unlink outcome.
        npub (str): Nostr npub that was unlinked.
    """

    status: UnlinkNostrIdentityResponse200DataStatus
    npub: str

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = UnlinkNostrIdentityResponse200DataStatus(d.pop("status"))

        npub = d.pop("npub")

        unlink_nostr_identity_response_200_data = cls(
            status=status,
            npub=npub,
        )

        return unlink_nostr_identity_response_200_data
