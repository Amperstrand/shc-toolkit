from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.update_nip_05_response_200_data_status import (
    UpdateNip05Response200DataStatus,
    check_update_nip_05_response_200_data_status,
)

T = TypeVar("T", bound="UpdateNip05Response200Data")


@_attrs_define
class UpdateNip05Response200Data:
    status: UpdateNip05Response200DataStatus
    """ NIP-05 update outcome. """
    nip05_name: str
    """ Stored NIP-05 local name. """
    npub: str
    """ Linked Nostr public key in npub form. """

    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        nip05_name = self.nip05_name

        npub = self.npub

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "nip05_name": nip05_name,
                "npub": npub,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = check_update_nip_05_response_200_data_status(d.pop("status"))

        nip05_name = d.pop("nip05_name")

        npub = d.pop("npub")

        update_nip_05_response_200_data = cls(
            status=status,
            nip05_name=nip05_name,
            npub=npub,
        )

        return update_nip_05_response_200_data
