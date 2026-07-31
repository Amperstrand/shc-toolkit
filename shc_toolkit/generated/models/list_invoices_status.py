from typing import Literal

ListInvoicesStatus = Literal["closed", "open", "past_due"]

LIST_INVOICES_STATUS_VALUES: set[ListInvoicesStatus] = {
    "closed",
    "open",
    "past_due",
}


def check_list_invoices_status(value: str) -> ListInvoicesStatus:
    if value in LIST_INVOICES_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_INVOICES_STATUS_VALUES!r}"
    )
