from typing import Literal

EventSubscriptionEventIdHeader = Literal["X-SHC-Webhook-Event-Id"]

EVENT_SUBSCRIPTION_EVENT_ID_HEADER_VALUES: set[EventSubscriptionEventIdHeader] = {
    "X-SHC-Webhook-Event-Id",
}


def check_event_subscription_event_id_header(
    value: str,
) -> EventSubscriptionEventIdHeader:
    if value in EVENT_SUBSCRIPTION_EVENT_ID_HEADER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_EVENT_ID_HEADER_VALUES!r}"
    )
