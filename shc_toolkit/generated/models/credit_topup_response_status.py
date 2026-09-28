from enum import StrEnum


class CreditTopupResponseStatus(StrEnum):
    CHECKOUT_REQUIRED = "checkout_required"

    def __str__(self) -> str:
        return str(self.value)
