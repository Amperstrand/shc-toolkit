from typing import Literal

EventSubscriptionCreatedSignatureHeader = Literal["X-SHC-Webhook-Signature"]

EVENT_SUBSCRIPTION_CREATED_SIGNATURE_HEADER_VALUES: set[
    EventSubscriptionCreatedSignatureHeader
] = {
    "X-SHC-Webhook-Signature",
}


def check_event_subscription_created_signature_header(
    value: str,
) -> EventSubscriptionCreatedSignatureHeader:
    if value in EVENT_SUBSCRIPTION_CREATED_SIGNATURE_HEADER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_CREATED_SIGNATURE_HEADER_VALUES!r}"
    )
