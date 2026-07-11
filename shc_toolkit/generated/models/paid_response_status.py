from enum import Enum


class PaidResponseStatus(str, Enum):
    PAID = "paid"

    def __str__(self) -> str:
        return str(self.value)
