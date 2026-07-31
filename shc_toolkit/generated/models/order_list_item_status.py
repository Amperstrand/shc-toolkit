from typing import Literal

OrderListItemStatus = Literal["accepted", "canceled", "fraud", "pending"]

ORDER_LIST_ITEM_STATUS_VALUES: set[OrderListItemStatus] = {
    "accepted",
    "canceled",
    "fraud",
    "pending",
}


def check_order_list_item_status(value: str) -> OrderListItemStatus:
    if value in ORDER_LIST_ITEM_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORDER_LIST_ITEM_STATUS_VALUES!r}"
    )
