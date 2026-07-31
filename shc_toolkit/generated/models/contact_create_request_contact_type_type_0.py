from typing import Literal

ContactCreateRequestContactTypeType0 = Literal["billing", "other"]

CONTACT_CREATE_REQUEST_CONTACT_TYPE_TYPE_0_VALUES: set[
    ContactCreateRequestContactTypeType0
] = {
    "billing",
    "other",
}


def check_contact_create_request_contact_type_type_0(
    value: str,
) -> ContactCreateRequestContactTypeType0:
    if value in CONTACT_CREATE_REQUEST_CONTACT_TYPE_TYPE_0_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CONTACT_CREATE_REQUEST_CONTACT_TYPE_TYPE_0_VALUES!r}"
    )
