from typing import Literal

ListClientDocumentsOrder = Literal["asc", "desc"]

LIST_CLIENT_DOCUMENTS_ORDER_VALUES: set[ListClientDocumentsOrder] = {
    "asc",
    "desc",
}


def check_list_client_documents_order(value: str) -> ListClientDocumentsOrder:
    if value in LIST_CLIENT_DOCUMENTS_ORDER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_CLIENT_DOCUMENTS_ORDER_VALUES!r}"
    )
