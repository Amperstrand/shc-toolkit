from typing import Literal

PaidResponseStatus = Literal["paid"]

PAID_RESPONSE_STATUS_VALUES: set[PaidResponseStatus] = {
    "paid",
}


def check_paid_response_status(value: str) -> PaidResponseStatus:
    if value in PAID_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PAID_RESPONSE_STATUS_VALUES!r}"
    )
