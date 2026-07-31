from typing import Literal

ListQuotationsStatus = Literal[
    "all", "approved", "dead", "draft", "expired", "invoiced", "lost", "pending"
]

LIST_QUOTATIONS_STATUS_VALUES: set[ListQuotationsStatus] = {
    "all",
    "approved",
    "dead",
    "draft",
    "expired",
    "invoiced",
    "lost",
    "pending",
}


def check_list_quotations_status(value: str) -> ListQuotationsStatus:
    if value in LIST_QUOTATIONS_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_QUOTATIONS_STATUS_VALUES!r}"
    )
