from typing import Literal

EventSubscriptionDeliveryIdHeader = Literal["X-SHC-Webhook-Delivery-Id"]

EVENT_SUBSCRIPTION_DELIVERY_ID_HEADER_VALUES: set[EventSubscriptionDeliveryIdHeader] = {
    "X-SHC-Webhook-Delivery-Id",
}


def check_event_subscription_delivery_id_header(
    value: str,
) -> EventSubscriptionDeliveryIdHeader:
    if value in EVENT_SUBSCRIPTION_DELIVERY_ID_HEADER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_DELIVERY_ID_HEADER_VALUES!r}"
    )
