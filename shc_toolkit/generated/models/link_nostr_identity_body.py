from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="LinkNostrIdentityBody")


@_attrs_define
class LinkNostrIdentityBody:
    """
    Attributes:
        public_key (str):
        challenge_id (str):
        signature (str):
        relay (str | Unset):
    """

    public_key: str
    challenge_id: str
    signature: str
    relay: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        public_key = self.public_key

        challenge_id = self.challenge_id

        signature = self.signature

        relay = self.relay

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "publicKey": public_key,
                "challengeId": challenge_id,
                "signature": signature,
            }
        )
        if relay is not UNSET:
            field_dict["relay"] = relay

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        public_key = d.pop("publicKey")

        challenge_id = d.pop("challengeId")

        signature = d.pop("signature")

        relay = d.pop("relay", UNSET)

        link_nostr_identity_body = cls(
            public_key=public_key,
            challenge_id=challenge_id,
            signature=signature,
            relay=relay,
        )

        return link_nostr_identity_body
