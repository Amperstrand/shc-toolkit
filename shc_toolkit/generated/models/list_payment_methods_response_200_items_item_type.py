from typing import Literal

ListPaymentMethodsResponse200ItemsItemType = Literal["ach", "cc"]

LIST_PAYMENT_METHODS_RESPONSE_200_ITEMS_ITEM_TYPE_VALUES: set[
    ListPaymentMethodsResponse200ItemsItemType
] = {
    "ach",
    "cc",
}


def check_list_payment_methods_response_200_items_item_type(
    value: str,
) -> ListPaymentMethodsResponse200ItemsItemType:
    if value in LIST_PAYMENT_METHODS_RESPONSE_200_ITEMS_ITEM_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_PAYMENT_METHODS_RESPONSE_200_ITEMS_ITEM_TYPE_VALUES!r}"
    )
