from typing import Literal

GetOrderResponse200DataStatus = Literal["accepted", "canceled", "fraud", "pending"]

GET_ORDER_RESPONSE_200_DATA_STATUS_VALUES: set[GetOrderResponse200DataStatus] = {
    "accepted",
    "canceled",
    "fraud",
    "pending",
}


def check_get_order_response_200_data_status(
    value: str,
) -> GetOrderResponse200DataStatus:
    if value in GET_ORDER_RESPONSE_200_DATA_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_ORDER_RESPONSE_200_DATA_STATUS_VALUES!r}"
    )
