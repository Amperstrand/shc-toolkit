from typing import Literal

QuotationSummaryStatusType1 = Literal[
    "approved", "dead", "draft", "expired", "invoiced", "lost", "pending"
]

QUOTATION_SUMMARY_STATUS_TYPE_1_VALUES: set[QuotationSummaryStatusType1] = {
    "approved",
    "dead",
    "draft",
    "expired",
    "invoiced",
    "lost",
    "pending",
}


def check_quotation_summary_status_type_1(value: str) -> QuotationSummaryStatusType1:
    if value in QUOTATION_SUMMARY_STATUS_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {QUOTATION_SUMMARY_STATUS_TYPE_1_VALUES!r}"
    )
