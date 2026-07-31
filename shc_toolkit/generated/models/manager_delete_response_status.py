from typing import Literal

ManagerDeleteResponseStatus = Literal["declined"]

MANAGER_DELETE_RESPONSE_STATUS_VALUES: set[ManagerDeleteResponseStatus] = {
    "declined",
}


def check_manager_delete_response_status(value: str) -> ManagerDeleteResponseStatus:
    if value in MANAGER_DELETE_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MANAGER_DELETE_RESPONSE_STATUS_VALUES!r}"
    )
