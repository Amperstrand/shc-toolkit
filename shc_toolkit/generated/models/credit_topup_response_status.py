from typing import Literal

CreditTopupResponseStatus = Literal["checkout_required"]

CREDIT_TOPUP_RESPONSE_STATUS_VALUES: set[CreditTopupResponseStatus] = {
    "checkout_required",
}


def check_credit_topup_response_status(value: str) -> CreditTopupResponseStatus:
    if value in CREDIT_TOPUP_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREDIT_TOPUP_RESPONSE_STATUS_VALUES!r}"
    )
