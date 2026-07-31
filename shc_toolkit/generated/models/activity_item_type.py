from typing import Literal

ActivityItemType = Literal[
    "contact_change", "login", "login_failed", "setting_change", "transaction"
]

ACTIVITY_ITEM_TYPE_VALUES: set[ActivityItemType] = {
    "contact_change",
    "login",
    "login_failed",
    "setting_change",
    "transaction",
}


def check_activity_item_type(value: str) -> ActivityItemType:
    if value in ACTIVITY_ITEM_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACTIVITY_ITEM_TYPE_VALUES!r}"
    )
