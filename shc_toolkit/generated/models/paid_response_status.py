from enum import StrEnum


class PaidResponseStatus(StrEnum):
    PAID = "paid"

    def __str__(self) -> str:
        return str(self.value)
