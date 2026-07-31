from typing import Literal

GetContactResponse200DataContactType = Literal["billing", "other", "primary"]

GET_CONTACT_RESPONSE_200_DATA_CONTACT_TYPE_VALUES: set[
    GetContactResponse200DataContactType
] = {
    "billing",
    "other",
    "primary",
}


def check_get_contact_response_200_data_contact_type(
    value: str,
) -> GetContactResponse200DataContactType:
    if value in GET_CONTACT_RESPONSE_200_DATA_CONTACT_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_CONTACT_RESPONSE_200_DATA_CONTACT_TYPE_VALUES!r}"
    )
