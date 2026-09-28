from enum import StrEnum


class GetSupportTicketResponse200DataStatus(StrEnum):
    AWAITING_REPLY = "awaiting_reply"
    CLOSED = "closed"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
