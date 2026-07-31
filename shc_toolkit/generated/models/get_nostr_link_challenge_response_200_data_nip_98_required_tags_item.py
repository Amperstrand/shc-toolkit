from typing import Literal

GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem = Literal[
    "challenge", "method", "u"
]

GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_REQUIRED_TAGS_ITEM_VALUES: set[
    GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem
] = {
    "challenge",
    "method",
    "u",
}


def check_get_nostr_link_challenge_response_200_data_nip_98_required_tags_item(
    value: str,
) -> GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem:
    if (
        value
        in GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_REQUIRED_TAGS_ITEM_VALUES
    ):
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_NOSTR_LINK_CHALLENGE_RESPONSE_200_DATA_NIP_98_REQUIRED_TAGS_ITEM_VALUES!r}"
    )
