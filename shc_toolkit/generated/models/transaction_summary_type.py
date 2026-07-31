from typing import Literal

TransactionSummaryType = Literal["ach", "cc", "other"]

TRANSACTION_SUMMARY_TYPE_VALUES: set[TransactionSummaryType] = {
    "ach",
    "cc",
    "other",
}


def check_transaction_summary_type(value: str) -> TransactionSummaryType:
    if value in TRANSACTION_SUMMARY_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRANSACTION_SUMMARY_TYPE_VALUES!r}"
    )
