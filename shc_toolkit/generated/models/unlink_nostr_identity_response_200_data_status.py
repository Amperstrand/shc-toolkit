from typing import Literal

UnlinkNostrIdentityResponse200DataStatus = Literal["unlinked"]

UNLINK_NOSTR_IDENTITY_RESPONSE_200_DATA_STATUS_VALUES: set[
    UnlinkNostrIdentityResponse200DataStatus
] = {
    "unlinked",
}


def check_unlink_nostr_identity_response_200_data_status(
    value: str,
) -> UnlinkNostrIdentityResponse200DataStatus:
    if value in UNLINK_NOSTR_IDENTITY_RESPONSE_200_DATA_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {UNLINK_NOSTR_IDENTITY_RESPONSE_200_DATA_STATUS_VALUES!r}"
    )
