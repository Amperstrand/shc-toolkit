from typing import Literal

ListSupportDepartmentsResponse200ItemsItemFieldsItemType = Literal[
    "checkbox",
    "emergency",
    "password",
    "quantity",
    "radio",
    "select",
    "text",
    "textarea",
]

LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_FIELDS_ITEM_TYPE_VALUES: set[
    ListSupportDepartmentsResponse200ItemsItemFieldsItemType
] = {
    "checkbox",
    "emergency",
    "password",
    "quantity",
    "radio",
    "select",
    "text",
    "textarea",
}


def check_list_support_departments_response_200_items_item_fields_item_type(
    value: str,
) -> ListSupportDepartmentsResponse200ItemsItemFieldsItemType:
    if (
        value
        in LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_FIELDS_ITEM_TYPE_VALUES
    ):
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SUPPORT_DEPARTMENTS_RESPONSE_200_ITEMS_ITEM_FIELDS_ITEM_TYPE_VALUES!r}"
    )
