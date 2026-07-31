from typing import Literal

EventSubscriptionCreatedTimestampHeader = Literal["X-SHC-Webhook-Timestamp"]

EVENT_SUBSCRIPTION_CREATED_TIMESTAMP_HEADER_VALUES: set[
    EventSubscriptionCreatedTimestampHeader
] = {
    "X-SHC-Webhook-Timestamp",
}


def check_event_subscription_created_timestamp_header(
    value: str,
) -> EventSubscriptionCreatedTimestampHeader:
    if value in EVENT_SUBSCRIPTION_CREATED_TIMESTAMP_HEADER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_CREATED_TIMESTAMP_HEADER_VALUES!r}"
    )
