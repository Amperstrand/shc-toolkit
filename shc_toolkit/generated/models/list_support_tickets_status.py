from enum import Enum


class ListSupportTicketsStatus(str, Enum):
    ALL = "all"
    AWAITING_REPLY = "awaiting_reply"
    CLOSED = "closed"
    IN_PROGRESS = "in_progress"
    NOT_CLOSED = "not_closed"
    ON_HOLD = "on_hold"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
