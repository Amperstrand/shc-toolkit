from enum import StrEnum


class CancelPendingOrderResponse200DataStatus(StrEnum):
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str(self.value)
