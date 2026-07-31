from typing import Literal

GetSupportTicketResponse200DataPriority = Literal[
    "critical", "emergency", "high", "low", "medium"
]

GET_SUPPORT_TICKET_RESPONSE_200_DATA_PRIORITY_VALUES: set[
    GetSupportTicketResponse200DataPriority
] = {
    "critical",
    "emergency",
    "high",
    "low",
    "medium",
}


def check_get_support_ticket_response_200_data_priority(
    value: str,
) -> GetSupportTicketResponse200DataPriority:
    if value in GET_SUPPORT_TICKET_RESPONSE_200_DATA_PRIORITY_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_SUPPORT_TICKET_RESPONSE_200_DATA_PRIORITY_VALUES!r}"
    )
