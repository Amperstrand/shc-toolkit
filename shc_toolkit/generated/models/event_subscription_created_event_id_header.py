from enum import StrEnum


class EventSubscriptionCreatedEventIdHeader(StrEnum):
    X_SHC_WEBHOOK_EVENT_ID = "X-SHC-Webhook-Event-Id"

    def __str__(self) -> str:
        return str(self.value)
