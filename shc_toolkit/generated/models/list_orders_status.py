from enum import Enum


class ListOrdersStatus(str, Enum):
    ACCEPTED = "accepted"
    ALL = "all"
    CANCELED = "canceled"
    FRAUD = "fraud"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
