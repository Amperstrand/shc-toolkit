from typing import Literal

CheckoutRedirectResponseStatus = Literal["checkout_required"]

CHECKOUT_REDIRECT_RESPONSE_STATUS_VALUES: set[CheckoutRedirectResponseStatus] = {
    "checkout_required",
}


def check_checkout_redirect_response_status(
    value: str,
) -> CheckoutRedirectResponseStatus:
    if value in CHECKOUT_REDIRECT_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CHECKOUT_REDIRECT_RESPONSE_STATUS_VALUES!r}"
    )
