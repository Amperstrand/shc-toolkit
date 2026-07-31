from typing import Literal

RegisterRequestScope = Literal["operate", "read"]

REGISTER_REQUEST_SCOPE_VALUES: set[RegisterRequestScope] = {
    "operate",
    "read",
}


def check_register_request_scope(value: str) -> RegisterRequestScope:
    if value in REGISTER_REQUEST_SCOPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {REGISTER_REQUEST_SCOPE_VALUES!r}"
    )
