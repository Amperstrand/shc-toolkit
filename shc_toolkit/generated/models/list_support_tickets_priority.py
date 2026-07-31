from typing import Literal

ListSupportTicketsPriority = Literal["critical", "emergency", "high", "low", "medium"]

LIST_SUPPORT_TICKETS_PRIORITY_VALUES: set[ListSupportTicketsPriority] = {
    "critical",
    "emergency",
    "high",
    "low",
    "medium",
}


def check_list_support_tickets_priority(value: str) -> ListSupportTicketsPriority:
    if value in LIST_SUPPORT_TICKETS_PRIORITY_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SUPPORT_TICKETS_PRIORITY_VALUES!r}"
    )
