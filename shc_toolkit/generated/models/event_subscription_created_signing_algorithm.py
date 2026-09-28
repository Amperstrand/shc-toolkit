from enum import StrEnum


class EventSubscriptionCreatedSigningAlgorithm(StrEnum):
    HMAC_SHA256 = "HMAC-SHA256"

    def __str__(self) -> str:
        return str(self.value)
