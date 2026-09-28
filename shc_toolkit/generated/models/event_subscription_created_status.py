from enum import StrEnum


class EventSubscriptionCreatedStatus(StrEnum):
    ACTIVE = "active"
    DEADLETTERED = "deadLettered"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
