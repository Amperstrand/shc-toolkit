from typing import Literal

ContactCreateResponseContactType = Literal["billing", "other"]

CONTACT_CREATE_RESPONSE_CONTACT_TYPE_VALUES: set[ContactCreateResponseContactType] = {
    "billing",
    "other",
}


def check_contact_create_response_contact_type(
    value: str,
) -> ContactCreateResponseContactType:
    if value in CONTACT_CREATE_RESPONSE_CONTACT_TYPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CONTACT_CREATE_RESPONSE_CONTACT_TYPE_VALUES!r}"
    )
