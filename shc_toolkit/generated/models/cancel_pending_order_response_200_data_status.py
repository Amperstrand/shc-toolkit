from typing import Literal

CancelPendingOrderResponse200DataStatus = Literal["canceled"]

CANCEL_PENDING_ORDER_RESPONSE_200_DATA_STATUS_VALUES: set[
    CancelPendingOrderResponse200DataStatus
] = {
    "canceled",
}


def check_cancel_pending_order_response_200_data_status(
    value: str,
) -> CancelPendingOrderResponse200DataStatus:
    if value in CANCEL_PENDING_ORDER_RESPONSE_200_DATA_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CANCEL_PENDING_ORDER_RESPONSE_200_DATA_STATUS_VALUES!r}"
    )
