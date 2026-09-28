from enum import StrEnum


class ListInvoicesStatus(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    PAST_DUE = "past_due"

    def __str__(self) -> str:
        return str(self.value)
