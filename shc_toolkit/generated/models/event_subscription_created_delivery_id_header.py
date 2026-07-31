from typing import Literal

EventSubscriptionCreatedDeliveryIdHeader = Literal["X-SHC-Webhook-Delivery-Id"]

EVENT_SUBSCRIPTION_CREATED_DELIVERY_ID_HEADER_VALUES: set[
    EventSubscriptionCreatedDeliveryIdHeader
] = {
    "X-SHC-Webhook-Delivery-Id",
}


def check_event_subscription_created_delivery_id_header(
    value: str,
) -> EventSubscriptionCreatedDeliveryIdHeader:
    if value in EVENT_SUBSCRIPTION_CREATED_DELIVERY_ID_HEADER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_CREATED_DELIVERY_ID_HEADER_VALUES!r}"
    )
