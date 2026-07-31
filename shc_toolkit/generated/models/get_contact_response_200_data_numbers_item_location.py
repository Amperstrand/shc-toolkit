from typing import Literal

GetContactResponse200DataNumbersItemLocation = Literal["home", "mobile", "work"]

GET_CONTACT_RESPONSE_200_DATA_NUMBERS_ITEM_LOCATION_VALUES: set[
    GetContactResponse200DataNumbersItemLocation
] = {
    "home",
    "mobile",
    "work",
}


def check_get_contact_response_200_data_numbers_item_location(
    value: str,
) -> GetContactResponse200DataNumbersItemLocation:
    if value in GET_CONTACT_RESPONSE_200_DATA_NUMBERS_ITEM_LOCATION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_CONTACT_RESPONSE_200_DATA_NUMBERS_ITEM_LOCATION_VALUES!r}"
    )
