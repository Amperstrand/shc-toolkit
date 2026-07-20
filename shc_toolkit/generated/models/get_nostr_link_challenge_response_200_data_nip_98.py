from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.get_nostr_link_challenge_response_200_data_nip_98_kind import (
    GetNostrLinkChallengeResponse200DataNip98Kind,
)
from ..models.get_nostr_link_challenge_response_200_data_nip_98_max_event_age_seconds import (
    GetNostrLinkChallengeResponse200DataNip98MaxEventAgeSeconds,
)
from ..models.get_nostr_link_challenge_response_200_data_nip_98_required_tags_item import (
    GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem,
)

T = TypeVar("T", bound="GetNostrLinkChallengeResponse200DataNip98")


@_attrs_define
class GetNostrLinkChallengeResponse200DataNip98:
    """
    Attributes:
        kind (GetNostrLinkChallengeResponse200DataNip98Kind): NIP-98 event kind required for redemption.
        required_tags (list[GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem]): Tags the signed NIP-98 event
            must carry.
        max_event_age_seconds (GetNostrLinkChallengeResponse200DataNip98MaxEventAgeSeconds): Maximum accepted NIP-98
            event age.
        note (str): Handler-provided signing instruction.
    """

    kind: GetNostrLinkChallengeResponse200DataNip98Kind
    required_tags: list[GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem]
    max_event_age_seconds: GetNostrLinkChallengeResponse200DataNip98MaxEventAgeSeconds
    note: str

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        required_tags = []
        for required_tags_item_data in self.required_tags:
            required_tags_item = required_tags_item_data.value
            required_tags.append(required_tags_item)

        max_event_age_seconds = self.max_event_age_seconds.value

        note = self.note

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "required_tags": required_tags,
                "max_event_age_seconds": max_event_age_seconds,
                "note": note,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = GetNostrLinkChallengeResponse200DataNip98Kind(d.pop("kind"))

        required_tags = []
        _required_tags = d.pop("required_tags")
        for required_tags_item_data in _required_tags:
            required_tags_item = (
                GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem(
                    required_tags_item_data
                )
            )

            required_tags.append(required_tags_item)

        max_event_age_seconds = (
            GetNostrLinkChallengeResponse200DataNip98MaxEventAgeSeconds(
                d.pop("max_event_age_seconds")
            )
        )

        note = d.pop("note")

        get_nostr_link_challenge_response_200_data_nip_98 = cls(
            kind=kind,
            required_tags=required_tags,
            max_event_age_seconds=max_event_age_seconds,
            note=note,
        )

        return get_nostr_link_challenge_response_200_data_nip_98
