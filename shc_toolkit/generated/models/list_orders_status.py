from typing import Literal

ListOrdersStatus = Literal["accepted", "all", "canceled", "fraud", "pending"]

LIST_ORDERS_STATUS_VALUES: set[ListOrdersStatus] = {
    "accepted",
    "all",
    "canceled",
    "fraud",
    "pending",
}


def check_list_orders_status(value: str) -> ListOrdersStatus:
    if value in LIST_ORDERS_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_ORDERS_STATUS_VALUES!r}"
    )
