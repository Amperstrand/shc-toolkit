from typing import Literal

ManagerInviteResponseStatus = Literal["invalid", "pending"]

MANAGER_INVITE_RESPONSE_STATUS_VALUES: set[ManagerInviteResponseStatus] = {
    "invalid",
    "pending",
}


def check_manager_invite_response_status(value: str) -> ManagerInviteResponseStatus:
    if value in MANAGER_INVITE_RESPONSE_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MANAGER_INVITE_RESPONSE_STATUS_VALUES!r}"
    )
