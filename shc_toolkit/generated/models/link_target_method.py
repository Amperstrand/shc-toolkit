from typing import Literal

LinkTargetMethod = Literal["DELETE", "GET", "PATCH", "POST", "PUT"]

LINK_TARGET_METHOD_VALUES: set[LinkTargetMethod] = {
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
}


def check_link_target_method(value: str) -> LinkTargetMethod:
    if value in LINK_TARGET_METHOD_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LINK_TARGET_METHOD_VALUES!r}"
    )
