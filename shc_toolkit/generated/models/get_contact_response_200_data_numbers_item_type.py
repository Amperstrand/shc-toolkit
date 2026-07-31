from typing import Literal

GetContactResponse200DataNumbersItemType = Literal["fax", "phone"]

GET_CONTACT_RESPONSE_200_DATA_NUMBERS_ITEM_TYPE_VALUES: set[
    GetContactResponse200DataNumbersItemType
] = {
    "fax",
    "phone",
}


def check_get_contact_response_200_data_numbers_item_type(
    value: str,
) -> GetContactResponse200DataNumbersItemType:
    if value in GET_CONTACT_RESPONSE_200_DATA_NUMBERS_ITEM_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_CONTACT_RESPONSE_200_DATA_NUMBERS_ITEM_TYPE_VALUES!r}"
    )
