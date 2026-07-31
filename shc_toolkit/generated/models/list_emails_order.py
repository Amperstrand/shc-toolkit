from typing import Literal

ListEmailsOrder = Literal["asc", "desc"]

LIST_EMAILS_ORDER_VALUES: set[ListEmailsOrder] = {
    "asc",
    "desc",
}


def check_list_emails_order(value: str) -> ListEmailsOrder:
    if value in LIST_EMAILS_ORDER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_EMAILS_ORDER_VALUES!r}"
    )
