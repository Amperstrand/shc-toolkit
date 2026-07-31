from typing import Literal

GetNostrLinkChallengeResponse200DataNip98Kind = Literal[27235]

GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_KIND_VALUES: set[
    GetNostrLinkChallengeResponse200DataNip98Kind
] = {
    27235,
}


def check_get_nostr_link_challenge_response_200_data_nip_98_kind(
    value: int,
) -> GetNostrLinkChallengeResponse200DataNip98Kind:
    if value in GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_KIND_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_KIND_VALUES!r}"
    )
