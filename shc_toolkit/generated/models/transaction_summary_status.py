from typing import Literal

TransactionSummaryStatus = Literal[
    "approved", "declined", "error", "pending", "refunded", "returned", "void"
]

TRANSACTION_SUMMARY_STATUS_VALUES: set[TransactionSummaryStatus] = {
    "approved",
    "declined",
    "error",
    "pending",
    "refunded",
    "returned",
    "void",
}


def check_transaction_summary_status(value: str) -> TransactionSummaryStatus:
    if value in TRANSACTION_SUMMARY_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRANSACTION_SUMMARY_STATUS_VALUES!r}"
    )
