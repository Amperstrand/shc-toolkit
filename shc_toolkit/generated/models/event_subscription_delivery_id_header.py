from enum import Enum


class EventSubscriptionDeliveryIdHeader(str, Enum):
    X_SHC_WEBHOOK_DELIVERY_ID = "X-SHC-Webhook-Delivery-Id"

    def __str__(self) -> str:
        return str(self.value)
