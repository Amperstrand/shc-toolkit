from typing import Literal

ListApiKeysResponse200ItemsItemScope = Literal["full", "operate", "read"]

LIST_API_KEYS_RESPONSE_200_ITEMS_ITEM_SCOPE_VALUES: set[
    ListApiKeysResponse200ItemsItemScope
] = {
    "full",
    "operate",
    "read",
}


def check_list_api_keys_response_200_items_item_scope(
    value: str,
) -> ListApiKeysResponse200ItemsItemScope:
    if value in LIST_API_KEYS_RESPONSE_200_ITEMS_ITEM_SCOPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_API_KEYS_RESPONSE_200_ITEMS_ITEM_SCOPE_VALUES!r}"
    )
