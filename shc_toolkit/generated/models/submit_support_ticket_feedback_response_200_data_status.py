from typing import Literal

SubmitSupportTicketFeedbackResponse200DataStatus = Literal["closed"]

SUBMIT_SUPPORT_TICKET_FEEDBACK_RESPONSE_200_DATA_STATUS_VALUES: set[
    SubmitSupportTicketFeedbackResponse200DataStatus
] = {
    "closed",
}


def check_submit_support_ticket_feedback_response_200_data_status(
    value: str,
) -> SubmitSupportTicketFeedbackResponse200DataStatus:
    if value in SUBMIT_SUPPORT_TICKET_FEEDBACK_RESPONSE_200_DATA_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SUBMIT_SUPPORT_TICKET_FEEDBACK_RESPONSE_200_DATA_STATUS_VALUES!r}"
    )
