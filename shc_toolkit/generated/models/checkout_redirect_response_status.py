from enum import StrEnum


class CheckoutRedirectResponseStatus(StrEnum):
    CHECKOUT_REQUIRED = "checkout_required"

    def __str__(self) -> str:
        return str(self.value)
