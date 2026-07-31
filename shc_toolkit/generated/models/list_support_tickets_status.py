from typing import Literal

ListSupportTicketsStatus = Literal[
    "all", "awaiting_reply", "closed", "in_progress", "not_closed", "on_hold", "open"
]

LIST_SUPPORT_TICKETS_STATUS_VALUES: set[ListSupportTicketsStatus] = {
    "all",
    "awaiting_reply",
    "closed",
    "in_progress",
    "not_closed",
    "on_hold",
    "open",
}


def check_list_support_tickets_status(value: str) -> ListSupportTicketsStatus:
    if value in LIST_SUPPORT_TICKETS_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SUPPORT_TICKETS_STATUS_VALUES!r}"
    )
