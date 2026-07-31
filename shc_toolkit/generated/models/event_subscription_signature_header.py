from typing import Literal

EventSubscriptionSignatureHeader = Literal["X-SHC-Webhook-Signature"]

EVENT_SUBSCRIPTION_SIGNATURE_HEADER_VALUES: set[EventSubscriptionSignatureHeader] = {
    "X-SHC-Webhook-Signature",
}


def check_event_subscription_signature_header(
    value: str,
) -> EventSubscriptionSignatureHeader:
    if value in EVENT_SUBSCRIPTION_SIGNATURE_HEADER_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_SUBSCRIPTION_SIGNATURE_HEADER_VALUES!r}"
    )
