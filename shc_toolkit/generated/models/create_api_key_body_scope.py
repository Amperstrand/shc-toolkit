from typing import Literal

CreateApiKeyBodyScope = Literal["full", "operate", "read"]

CREATE_API_KEY_BODY_SCOPE_VALUES: set[CreateApiKeyBodyScope] = {
    "full",
    "operate",
    "read",
}


def check_create_api_key_body_scope(value: str) -> CreateApiKeyBodyScope:
    if value in CREATE_API_KEY_BODY_SCOPE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_API_KEY_BODY_SCOPE_VALUES!r}"
    )
