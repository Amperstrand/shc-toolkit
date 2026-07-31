from typing import Literal

InvoiceStatus = Literal[
    "draft", "open", "paid", "past_due", "pending", "scheduled", "voided"
]

INVOICE_STATUS_VALUES: set[InvoiceStatus] = {
    "draft",
    "open",
    "paid",
    "past_due",
    "pending",
    "scheduled",
    "voided",
}


def check_invoice_status(value: str) -> InvoiceStatus:
    if value in INVOICE_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {INVOICE_STATUS_VALUES!r}"
    )
