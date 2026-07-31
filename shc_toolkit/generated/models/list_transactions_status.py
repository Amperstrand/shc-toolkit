from typing import Literal

ListTransactionsStatus = Literal[
    "all", "approved", "declined", "error", "pending", "refunded", "returned", "void"
]

LIST_TRANSACTIONS_STATUS_VALUES: set[ListTransactionsStatus] = {
    "all",
    "approved",
    "declined",
    "error",
    "pending",
    "refunded",
    "returned",
    "void",
}


def check_list_transactions_status(value: str) -> ListTransactionsStatus:
    if value in LIST_TRANSACTIONS_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_TRANSACTIONS_STATUS_VALUES!r}"
    )
