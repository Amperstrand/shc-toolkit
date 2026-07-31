from typing import Literal

ListPaymentMethodsResponse200ItemsItemStatus = Literal[
    "active", "inactive", "unverified"
]

LIST_PAYMENT_METHODS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES: set[
    ListPaymentMethodsResponse200ItemsItemStatus
] = {
    "active",
    "inactive",
    "unverified",
}


def check_list_payment_methods_response_200_items_item_status(
    value: str,
) -> ListPaymentMethodsResponse200ItemsItemStatus:
    if value in LIST_PAYMENT_METHODS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_PAYMENT_METHODS_RESPONSE_200_ITEMS_ITEM_STATUS_VALUES!r}"
    )
