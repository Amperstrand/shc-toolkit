from typing import Literal

ActivityItemStatusType3Type1 = Literal[
    "approved", "declined", "error", "pending", "refunded", "returned", "void"
]

ACTIVITY_ITEM_STATUS_TYPE_3_TYPE_1_VALUES: set[ActivityItemStatusType3Type1] = {
    "approved",
    "declined",
    "error",
    "pending",
    "refunded",
    "returned",
    "void",
}


def check_activity_item_status_type_3_type_1(
    value: str,
) -> ActivityItemStatusType3Type1:
    if value in ACTIVITY_ITEM_STATUS_TYPE_3_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACTIVITY_ITEM_STATUS_TYPE_3_TYPE_1_VALUES!r}"
    )
