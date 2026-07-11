from enum import Enum


class CheckoutRedirectResponseStatus(str, Enum):
    CHECKOUT_REQUIRED = "checkout_required"

    def __str__(self) -> str:
        return str(self.value)
