from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UnlinkNostrIdentityBody")


@_attrs_define
class UnlinkNostrIdentityBody:
    """
    Attributes:
        public_key (str | Unset):
    """

    public_key: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        public_key = self.public_key

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if public_key is not UNSET:
            field_dict["publicKey"] = public_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        public_key = d.pop("publicKey", UNSET)

        unlink_nostr_identity_body = cls(
            public_key=public_key,
        )

        return unlink_nostr_identity_body
