from typing import Literal

GetNostrLinkChallengeResponse200DataExpiresInSeconds = Literal[300]

GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_EXPIRES_IN_SECONDS_VALUES: set[
    GetNostrLinkChallengeResponse200DataExpiresInSeconds
] = {
    300,
}


def check_get_nostr_link_challenge_response_200_data_expires_in_seconds(
    value: int,
) -> GetNostrLinkChallengeResponse200DataExpiresInSeconds:
    if value in GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_EXPIRES_IN_SECONDS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_EXPIRES_IN_SECONDS_VALUES!r}"
    )
