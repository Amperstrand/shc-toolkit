from enum import Enum


class SubmitSupportTicketFeedbackResponse200DataStatus(str, Enum):
    CLOSED = "closed"

    def __str__(self) -> str:
        return str(self.value)
