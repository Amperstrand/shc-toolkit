from typing import Literal

ListSupportTicketsResponse200ItemsItemPriority = Literal[
    "critical", "emergency", "high", "low", "medium"
]

LIST_SUPPORT_TICKETS_RESPONSE_200_ITEMS_ITEM_PRIORITY_VALUES: set[
    ListSupportTicketsResponse200ItemsItemPriority
] = {
    "critical",
    "emergency",
    "high",
    "low",
    "medium",
}


def check_list_support_tickets_response_200_items_item_priority(
    value: str,
) -> ListSupportTicketsResponse200ItemsItemPriority:
    if value in LIST_SUPPORT_TICKETS_RESPONSE_200_ITEMS_ITEM_PRIORITY_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SUPPORT_TICKETS_RESPONSE_200_ITEMS_ITEM_PRIORITY_VALUES!r}"
    )
