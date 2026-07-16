from enum import Enum


class EventSubscriptionCreatedStatus(str, Enum):
    ACTIVE = "active"
    DEADLETTERED = "deadLettered"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
