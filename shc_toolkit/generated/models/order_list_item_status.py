from enum import Enum


class OrderListItemStatus(str, Enum):
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    FRAUD = "fraud"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
