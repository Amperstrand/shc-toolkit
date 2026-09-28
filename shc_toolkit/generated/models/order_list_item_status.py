from enum import StrEnum


class OrderListItemStatus(StrEnum):
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    FRAUD = "fraud"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
