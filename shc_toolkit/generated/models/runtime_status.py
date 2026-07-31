from typing import Literal

RuntimeStatus = Literal["paused", "running", "stopped", "suspended", "unknown"]

RUNTIME_STATUS_VALUES: set[RuntimeStatus] = {
    "paused",
    "running",
    "stopped",
    "suspended",
    "unknown",
}


def check_runtime_status(value: str) -> RuntimeStatus:
    if value in RUNTIME_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {RUNTIME_STATUS_VALUES!r}"
    )
