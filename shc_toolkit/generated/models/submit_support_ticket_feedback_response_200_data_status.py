from enum import StrEnum


class SubmitSupportTicketFeedbackResponse200DataStatus(StrEnum):
    CLOSED = "closed"

    def __str__(self) -> str:
        return str(self.value)
