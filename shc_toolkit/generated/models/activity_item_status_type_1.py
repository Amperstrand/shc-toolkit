from typing import Literal

ActivityItemStatusType1 = Literal[
    "approved", "declined", "error", "pending", "refunded", "returned", "void"
]

ACTIVITY_ITEM_STATUS_TYPE_1_VALUES: set[ActivityItemStatusType1] = {
    "approved",
    "declined",
    "error",
    "pending",
    "refunded",
    "returned",
    "void",
}


def check_activity_item_status_type_1(value: str) -> ActivityItemStatusType1:
    if value in ACTIVITY_ITEM_STATUS_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACTIVITY_ITEM_STATUS_TYPE_1_VALUES!r}"
    )
