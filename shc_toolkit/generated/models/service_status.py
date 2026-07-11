from enum import Enum


class ServiceStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    IN_REVIEW = "in_review"
    ON_HOLD = "on_hold"
    PENDING = "pending"
    PENDING_CANCELLATION = "pending_cancellation"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
