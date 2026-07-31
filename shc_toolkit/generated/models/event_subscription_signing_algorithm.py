from typing import Literal

EventSubscriptionSigningAlgorithm = Literal["HMAC-SHA256"]

EVENT_SUBSCRIPTION_SIGNING_ALGORITHM_VALUES: set[EventSubscriptionSigningAlgorithm] = {
    "HMAC-SHA256",
}


def check_event_subscription_signing_algorithm(
    value: str,
) -> EventSubscriptionSigningAlgorithm:
    if value in EVENT_SUBSCRIPTION_SIGNING_ALGORITHM_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_SIGNING_ALGORITHM_VALUES!r}"
    )
