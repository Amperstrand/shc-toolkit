from typing import Literal

ListSupportDepartmentsResponse200ItemsItemPrioritiesItem = Literal[
    "critical", "emergency", "high", "low", "medium"
]

LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_PRIORITIES_ITEM_VALUES: set[
    ListSupportDepartmentsResponse200ItemsItemPrioritiesItem
] = {
    "critical",
    "emergency",
    "high",
    "low",
    "medium",
}


def check_list_support_departments_response_200_items_item_priorities_item(
    value: str,
) -> ListSupportDepartmentsResponse200ItemsItemPrioritiesItem:
    if value in LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_PRIORITIES_ITEM_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_PRIORITIES_ITEM_VALUES!r}"
    )
