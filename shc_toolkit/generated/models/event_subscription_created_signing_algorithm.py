from typing import Literal

EventSubscriptionCreatedSigningAlgorithm = Literal["HMAC-SHA256"]

EVENT_SUBSCRIPTION_CREATED_SIGNING_ALGORITHM_VALUES: set[
    EventSubscriptionCreatedSigningAlgorithm
] = {
    "HMAC-SHA256",
}


def check_event_subscription_created_signing_algorithm(
    value: str,
) -> EventSubscriptionCreatedSigningAlgorithm:
    if value in EVENT_SUBSCRIPTION_CREATED_SIGNING_ALGORITHM_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_CREATED_SIGNING_ALGORITHM_VALUES!r}"
    )
