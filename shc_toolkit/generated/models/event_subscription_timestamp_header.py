from typing import Literal

EventSubscriptionTimestampHeader = Literal["X-SHC-Webhook-Timestamp"]

EVENT_SUBSCRIPTION_TIMESTAMP_HEADER_VALUES: set[EventSubscriptionTimestampHeader] = {
    "X-SHC-Webhook-Timestamp",
}


def check_event_subscription_timestamp_header(
    value: str,
) -> EventSubscriptionTimestampHeader:
    if value in EVENT_SUBSCRIPTION_TIMESTAMP_HEADER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_TIMESTAMP_HEADER_VALUES!r}"
    )
