from typing import Literal

RegisterApiKeyScope = Literal["operate", "read"]

REGISTER_API_KEY_SCOPE_VALUES: set[RegisterApiKeyScope] = {
    "operate",
    "read",
}


def check_register_api_key_scope(value: str) -> RegisterApiKeyScope:
    if value in REGISTER_API_KEY_SCOPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {REGISTER_API_KEY_SCOPE_VALUES!r}"
    )
