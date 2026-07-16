from enum import Enum


class EventSubscriptionSignatureHeader(str, Enum):
    X_SHC_WEBHOOK_SIGNATURE = "X-SHC-Webhook-Signature"

    def __str__(self) -> str:
        return str(self.value)
