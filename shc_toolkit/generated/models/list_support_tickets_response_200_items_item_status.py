from typing import Literal

ListSupportTicketsResponse200ItemsItemStatus = Literal[
    "awaiting_reply", "closed", "in_progress", "on_hold", "open"
]

LIST_SUPPORT_TICKETS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES: set[
    ListSupportTicketsResponse200ItemsItemStatus
] = {
    "awaiting_reply",
    "closed",
    "in_progress",
    "on_hold",
    "open",
}


def check_list_support_tickets_response_200_items_item_status(
    value: str,
) -> ListSupportTicketsResponse200ItemsItemStatus:
    if value in LIST_SUPPORT_TICKETS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SUPPORT_TICKETS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES!r}"
    )
