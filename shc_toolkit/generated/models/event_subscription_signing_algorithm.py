from enum import Enum


class EventSubscriptionSigningAlgorithm(str, Enum):
    HMAC_SHA256 = "HMAC-SHA256"

    def __str__(self) -> str:
        return str(self.value)
