from typing import Literal

ErrorDetailCode = Literal[
    "already_in_use",
    "invalid",
    "out_of_range",
    "required",
    "unknown_field",
    "unsupported_value",
]

ERROR_DETAIL_CODE_VALUES: set[ErrorDetailCode] = {
    "already_in_use",
    "invalid",
    "out_of_range",
    "required",
    "unknown_field",
    "unsupported_value",
}


def check_error_detail_code(value: str) -> ErrorDetailCode:
    if value in ERROR_DETAIL_CODE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ERROR_DETAIL_CODE_VALUES!r}"
    )
