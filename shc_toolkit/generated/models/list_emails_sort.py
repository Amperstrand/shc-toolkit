from typing import Literal

ListEmailsSort = Literal["date_sent", "subject"]

LIST_EMAILS_SORT_VALUES: set[ListEmailsSort] = {
    "date_sent",
    "subject",
}


def check_list_emails_sort(value: str) -> ListEmailsSort:
    if value in LIST_EMAILS_SORT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_EMAILS_SORT_VALUES!r}"
    )
