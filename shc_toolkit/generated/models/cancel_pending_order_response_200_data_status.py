from enum import Enum


class CancelPendingOrderResponse200DataStatus(str, Enum):
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str(self.value)
