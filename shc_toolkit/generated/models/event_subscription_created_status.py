from typing import Literal

EventSubscriptionCreatedStatus = Literal["active", "deadLettered", "paused"]

EVENT_SUBSCRIPTION_CREATED_STATUS_VALUES: set[EventSubscriptionCreatedStatus] = {
    "active",
    "deadLettered",
    "paused",
}


def check_event_subscription_created_status(
    value: str,
) -> EventSubscriptionCreatedStatus:
    if value in EVENT_SUBSCRIPTION_CREATED_STATUS_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_CREATED_STATUS_VALUES!r}"
    )
