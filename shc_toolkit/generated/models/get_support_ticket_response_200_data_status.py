from typing import Literal

GetSupportTicketResponse200DataStatus = Literal[
    "awaiting_reply", "closed", "in_progress", "on_hold", "open"
]

GET_SUPPORT_TICKET_RESPONSE_200_DATA_STATUS_VALUES: set[
    GetSupportTicketResponse200DataStatus
] = {
    "awaiting_reply",
    "closed",
    "in_progress",
    "on_hold",
    "open",
}


def check_get_support_ticket_response_200_data_status(
    value: str,
) -> GetSupportTicketResponse200DataStatus:
    if value in GET_SUPPORT_TICKET_RESPONSE_200_DATA_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_SUPPORT_TICKET_RESPONSE_200_DATA_STATUS_VALUES!r}"
    )
