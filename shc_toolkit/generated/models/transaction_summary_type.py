from enum import StrEnum


class TransactionSummaryType(StrEnum):
    ACH = "ach"
    CC = "cc"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
