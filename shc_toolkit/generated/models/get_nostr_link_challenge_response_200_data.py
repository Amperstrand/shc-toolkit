from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.get_nostr_link_challenge_response_200_data_expires_in_seconds import (
    GetNostrLinkChallengeResponse200DataExpiresInSeconds,
    check_get_nostr_link_challenge_response_200_data_expires_in_seconds,
)

if TYPE_CHECKING:
    from ..models.get_nostr_link_challenge_response_200_data_nip_98 import (
        GetNostrLinkChallengeResponse200DataNip98,
    )


T = TypeVar("T", bound="GetNostrLinkChallengeResponse200Data")


@_attrs_define
class GetNostrLinkChallengeResponse200Data:
    challenge: str
    """ One-time Nostr link/unlink challenge nonce. """
    expires_in_seconds: GetNostrLinkChallengeResponse200DataExpiresInSeconds
    """ Seconds until the challenge expires. """
    single_use: bool
    """ Whether the challenge is consumed on redemption. """
    linked: bool
    """ Whether this account currently has a linked Nostr identity. """
    npub: None | str
    """ Currently linked npub, or null when no Nostr identity is linked. """
    nip98: GetNostrLinkChallengeResponse200DataNip98

    def to_dict(self) -> dict[str, Any]:
        challenge = self.challenge

        expires_in_seconds: int = self.expires_in_seconds

        single_use = self.single_use

        linked = self.linked

        npub: None | str
        npub = self.npub

        nip98 = self.nip98.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "challenge": challenge,
                "expires_in_seconds": expires_in_seconds,
                "single_use": single_use,
                "linked": linked,
                "npub": npub,
                "nip98": nip98,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_nostr_link_challenge_response_200_data_nip_98 import (
            GetNostrLinkChallengeResponse200DataNip98,
        )

        d = dict(src_dict)
        challenge = d.pop("challenge")

        expires_in_seconds = (
            check_get_nostr_link_challenge_response_200_data_expires_in_seconds(
                d.pop("expires_in_seconds")
            )
        )

        single_use = d.pop("single_use")

        linked = d.pop("linked")

        def _parse_npub(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        npub = _parse_npub(d.pop("npub"))

        nip98 = GetNostrLinkChallengeResponse200DataNip98.from_dict(d.pop("nip98"))

        get_nostr_link_challenge_response_200_data = cls(
            challenge=challenge,
            expires_in_seconds=expires_in_seconds,
            single_use=single_use,
            linked=linked,
            npub=npub,
            nip98=nip98,
        )

        return get_nostr_link_challenge_response_200_data
