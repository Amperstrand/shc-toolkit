from typing import Literal

LinkNostrIdentityResponse200DataStatus = Literal["already_linked", "linked"]

LINK_NOSTR_IDENTITY_RESPONSE_200_DATA_STATUS_VALUES: set[
    LinkNostrIdentityResponse200DataStatus
] = {
    "already_linked",
    "linked",
}


def check_link_nostr_identity_response_200_data_status(
    value: str,
) -> LinkNostrIdentityResponse200DataStatus:
    if value in LINK_NOSTR_IDENTITY_RESPONSE_200_DATA_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LINK_NOSTR_IDENTITY_RESPONSE_200_DATA_STATUS_VALUES!r}"
    )
