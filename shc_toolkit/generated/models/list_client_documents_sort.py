from typing import Literal

ListClientDocumentsSort = Literal["date_added", "name"]

LIST_CLIENT_DOCUMENTS_SORT_VALUES: set[ListClientDocumentsSort] = {
    "date_added",
    "name",
}


def check_list_client_documents_sort(value: str) -> ListClientDocumentsSort:
    if value in LIST_CLIENT_DOCUMENTS_SORT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_CLIENT_DOCUMENTS_SORT_VALUES!r}"
    )
