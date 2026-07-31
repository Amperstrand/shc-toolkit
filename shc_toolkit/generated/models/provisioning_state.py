from typing import Literal

ProvisioningState = Literal[
    "canceled", "on_hold", "pending", "provisioning", "ready", "suspended"
]

PROVISIONING_STATE_VALUES: set[ProvisioningState] = {
    "canceled",
    "on_hold",
    "pending",
    "provisioning",
    "ready",
    "suspended",
}


def check_provisioning_state(value: str) -> ProvisioningState:
    if value in PROVISIONING_STATE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROVISIONING_STATE_VALUES!r}"
    )
