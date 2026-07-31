from typing import Literal

EventSubscriptionCreatedEventIdHeader = Literal["X-SHC-Webhook-Event-Id"]

EVENT_SUBSCRIPTION_CREATED_EVENT_ID_HEADER_VALUES: set[
    EventSubscriptionCreatedEventIdHeader
] = {
    "X-SHC-Webhook-Event-Id",
}


def check_event_subscription_created_event_id_header(
    value: str,
) -> EventSubscriptionCreatedEventIdHeader:
    if value in EVENT_SUBSCRIPTION_CREATED_EVENT_ID_HEADER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_CREATED_EVENT_ID_HEADER_VALUES!r}"
    )
