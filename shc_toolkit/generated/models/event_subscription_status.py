from typing import Literal

EventSubscriptionStatus = Literal["active", "deadLettered", "paused"]

EVENT_SUBSCRIPTION_STATUS_VALUES: set[EventSubscriptionStatus] = {
    "active",
    "deadLettered",
    "paused",
}


def check_event_subscription_status(value: str) -> EventSubscriptionStatus:
    if value in EVENT_SUBSCRIPTION_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_STATUS_VALUES!r}"
    )
