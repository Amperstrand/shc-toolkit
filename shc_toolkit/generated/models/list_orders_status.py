from enum import StrEnum


class ListOrdersStatus(StrEnum):
    ACCEPTED = "accepted"
    ALL = "all"
    CANCELED = "canceled"
    FRAUD = "fraud"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
