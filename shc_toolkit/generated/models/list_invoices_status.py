from enum import Enum


class ListInvoicesStatus(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    PAST_DUE = "past_due"

    def __str__(self) -> str:
        return str(self.value)
