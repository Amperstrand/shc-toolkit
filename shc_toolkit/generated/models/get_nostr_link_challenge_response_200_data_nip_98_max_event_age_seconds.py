from typing import Literal

GetNostrLinkChallengeResponse200DataNip98MaxEventAgeSeconds = Literal[600]

GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_MAX_EVENT_AGE_SECONDS_VALUES: set[
    GetNostrLinkChallengeResponse200DataNip98MaxEventAgeSeconds
] = {
    600,
}


def check_get_nostr_link_challenge_response_200_data_nip_98_max_event_age_seconds(
    value: int,
) -> GetNostrLinkChallengeResponse200DataNip98MaxEventAgeSeconds:
    if (
        value
        in GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_MAX_EVENT_AGE_SECONDS_VALUES
    ):
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_MAX_EVENT_AGE_SECONDS_VALUES!r}"
    )
