from typing import Literal

ListManagedAccountsResponse200ItemsItemStatus = Literal["active", "pending"]

LIST_MANAGED_ACCOUNTS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES: set[
    ListManagedAccountsResponse200ItemsItemStatus
] = {
    "active",
    "pending",
}


def check_list_managed_accounts_response_200_items_item_status(
    value: str,
) -> ListManagedAccountsResponse200ItemsItemStatus:
    if value in LIST_MANAGED_ACCOUNTS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_MANAGED_ACCOUNTS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES!r}"
    )
