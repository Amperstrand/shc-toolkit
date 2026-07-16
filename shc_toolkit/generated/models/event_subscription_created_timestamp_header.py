from enum import Enum


class EventSubscriptionCreatedTimestampHeader(str, Enum):
    X_SHC_WEBHOOK_TIMESTAMP = "X-SHC-Webhook-Timestamp"

    def __str__(self) -> str:
        return str(self.value)
