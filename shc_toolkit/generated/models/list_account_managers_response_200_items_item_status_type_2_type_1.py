from typing import Literal

ListAccountManagersResponse200ItemsItemStatusType2Type1 = Literal[
    "active", "invalid", "pending"
]

LIST_ACCOUNT_MANAGERS_RESPONSE_200_ITEMS_ITEM_STATUS_TYPE_2_TYPE_1_VALUES: set[
    ListAccountManagersResponse200ItemsItemStatusType2Type1
] = {
    "active",
    "invalid",
    "pending",
}


def check_list_account_managers_response_200_items_item_status_type_2_type_1(
    value: str,
) -> ListAccountManagersResponse200ItemsItemStatusType2Type1:
    if (
        value
        in LIST_ACCOUNT_MANAGERS_RESPONSE_200_ITEMS_ITEM_STATUS_TYPE_2_TYPE_1_VALUES
    ):
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_ACCOUNT_MANAGERS_RESPONSE_200_ITEMS_ITEM_STATUS_TYPE_2_TYPE_1_VALUES!r}"
    )
