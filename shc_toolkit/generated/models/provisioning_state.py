from enum import Enum


class ProvisioningState(str, Enum):
    CANCELED = "canceled"
    ON_HOLD = "on_hold"
    PENDING = "pending"
    PROVISIONING = "provisioning"
    READY = "ready"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
