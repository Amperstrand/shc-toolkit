from typing import Literal

ListSupportDepartmentsResponse200ItemsItemDefaultPriority = Literal[
    "critical", "emergency", "high", "low", "medium"
]

LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_DEFAULT_PRIORITY_VALUES: set[
    ListSupportDepartmentsResponse200ItemsItemDefaultPriority
] = {
    "critical",
    "emergency",
    "high",
    "low",
    "medium",
}


def check_list_support_departments_response_200_items_item_default_priority(
    value: str,
) -> ListSupportDepartmentsResponse200ItemsItemDefaultPriority:
    if (
        value
        in LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_DEFAULT_PRIORITY_VALUES
    ):
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_DEFAULT_PRIORITY_VALUES!r}"
    )
