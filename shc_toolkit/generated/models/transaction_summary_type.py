from enum import Enum


class TransactionSummaryType(str, Enum):
    ACH = "ach"
    CC = "cc"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
