from enum import Enum


class ListSupportTicketsResponse200ItemsItemStatus(str, Enum):
    AWAITING_REPLY = "awaiting_reply"
    CLOSED = "closed"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
