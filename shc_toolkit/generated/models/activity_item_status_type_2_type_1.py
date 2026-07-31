from typing import Literal

ActivityItemStatusType2Type1 = Literal[
    "approved", "declined", "error", "pending", "refunded", "returned", "void"
]

ACTIVITY_ITEM_STATUS_TYPE_2_TYPE_1_VALUES: set[ActivityItemStatusType2Type1] = {
    "approved",
    "declined",
    "error",
    "pending",
    "refunded",
    "returned",
    "void",
}


def check_activity_item_status_type_2_type_1(
    value: str,
) -> ActivityItemStatusType2Type1:
    if value in ACTIVITY_ITEM_STATUS_TYPE_2_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACTIVITY_ITEM_STATUS_TYPE_2_TYPE_1_VALUES!r}"
    )
