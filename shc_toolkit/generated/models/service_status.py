from typing import Literal

ServiceStatus = Literal[
    "active",
    "canceled",
    "in_review",
    "on_hold",
    "pending",
    "pending_cancellation",
    "suspended",
]

SERVICE_STATUS_VALUES: set[ServiceStatus] = {
    "active",
    "canceled",
    "in_review",
    "on_hold",
    "pending",
    "pending_cancellation",
    "suspended",
}


def check_service_status(value: str) -> ServiceStatus:
    if value in SERVICE_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SERVICE_STATUS_VALUES!r}"
    )
