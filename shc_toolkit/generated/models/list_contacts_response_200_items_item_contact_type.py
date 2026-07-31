from typing import Literal

ListContactsResponse200ItemsItemContactType = Literal["billing", "other", "primary"]

LIST_CONTACTS_RESPONSE_200_ITEMS_ITEM_CONTACT_TYPE_VALUES: set[
    ListContactsResponse200ItemsItemContactType
] = {
    "billing",
    "other",
    "primary",
}


def check_list_contacts_response_200_items_item_contact_type(
    value: str,
) -> ListContactsResponse200ItemsItemContactType:
    if value in LIST_CONTACTS_RESPONSE_200_ITEMS_ITEM_CONTACT_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_CONTACTS_RESPONSE_200_ITEMS_ITEM_CONTACT_TYPE_VALUES!r}"
    )
