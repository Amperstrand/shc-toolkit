from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.event_subscription_delivery_id_header import (
    EventSubscriptionDeliveryIdHeader,
)
from ..models.event_subscription_event_id_header import EventSubscriptionEventIdHeader
from ..models.event_subscription_signature_header import (
    EventSubscriptionSignatureHeader,
)
from ..models.event_subscription_signing_algorithm import (
    EventSubscriptionSigningAlgorithm,
)
from ..models.event_subscription_status import EventSubscriptionStatus
from ..models.event_subscription_timestamp_header import (
    EventSubscriptionTimestampHeader,
)

T = TypeVar("T", bound="EventSubscription")


@_attrs_define
class EventSubscription:
    """Webhook subscription metadata. The signing secret is not present on read, list, delete, or idempotent replay
    responses.

        Attributes:
            event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.
            url (str): Registered HTTPS webhook destination. Example: https://hooks.customer-domain.com/shc/webhooks.
            event_types (list[str]): CloudEvents type filters matched against the customer-scoped /events feed.
            signing_algorithm (EventSubscriptionSigningAlgorithm):  Example: HMAC-SHA256.
            signature_header (EventSubscriptionSignatureHeader):  Example: X-SHC-Webhook-Signature.
            timestamp_header (EventSubscriptionTimestampHeader):  Example: X-SHC-Webhook-Timestamp.
            event_id_header (EventSubscriptionEventIdHeader):  Example: X-SHC-Webhook-Event-Id.
            delivery_id_header (EventSubscriptionDeliveryIdHeader):  Example: X-SHC-Webhook-Delivery-Id.
            status (EventSubscriptionStatus):  Example: active.
            secret_preview (str): Display-only prefix. It is not enough to verify signatures. Example: whsec_abc123....
            created_at (datetime.datetime):  Example: 2026-07-13T22:30:00Z.
            updated_at (datetime.datetime):  Example: 2026-07-13T22:30:00Z.
            last_delivery_at (datetime.datetime | None):  Example: 2026-07-13T22:31:00Z.
            dead_letter_count (int):
    """

    event_subscription_id: str
    url: str
    event_types: list[str]
    signing_algorithm: EventSubscriptionSigningAlgorithm
    signature_header: EventSubscriptionSignatureHeader
    timestamp_header: EventSubscriptionTimestampHeader
    event_id_header: EventSubscriptionEventIdHeader
    delivery_id_header: EventSubscriptionDeliveryIdHeader
    status: EventSubscriptionStatus
    secret_preview: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_delivery_at: datetime.datetime | None
    dead_letter_count: int

    def to_dict(self) -> dict[str, Any]:
        event_subscription_id = self.event_subscription_id

        url = self.url

        event_types = self.event_types

        signing_algorithm = self.signing_algorithm.value

        signature_header = self.signature_header.value

        timestamp_header = self.timestamp_header.value

        event_id_header = self.event_id_header.value

        delivery_id_header = self.delivery_id_header.value

        status = self.status.value

        secret_preview = self.secret_preview

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        last_delivery_at: None | str
        if isinstance(self.last_delivery_at, datetime.datetime):
            last_delivery_at = self.last_delivery_at.isoformat()
        else:
            last_delivery_at = self.last_delivery_at

        dead_letter_count = self.dead_letter_count

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "eventSubscriptionId": event_subscription_id,
                "url": url,
                "eventTypes": event_types,
                "signingAlgorithm": signing_algorithm,
                "signatureHeader": signature_header,
                "timestampHeader": timestamp_header,
                "eventIdHeader": event_id_header,
                "deliveryIdHeader": delivery_id_header,
                "status": status,
                "secretPreview": secret_preview,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "lastDeliveryAt": last_delivery_at,
                "deadLetterCount": dead_letter_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        event_subscription_id = d.pop("eventSubscriptionId")

        url = d.pop("url")

        event_types = cast(list[str], d.pop("eventTypes"))

        signing_algorithm = EventSubscriptionSigningAlgorithm(d.pop("signingAlgorithm"))

        signature_header = EventSubscriptionSignatureHeader(d.pop("signatureHeader"))

        timestamp_header = EventSubscriptionTimestampHeader(d.pop("timestampHeader"))

        event_id_header = EventSubscriptionEventIdHeader(d.pop("eventIdHeader"))

        delivery_id_header = EventSubscriptionDeliveryIdHeader(
            d.pop("deliveryIdHeader")
        )

        status = EventSubscriptionStatus(d.pop("status"))

        secret_preview = d.pop("secretPreview")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        def _parse_last_delivery_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_delivery_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_delivery_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_delivery_at = _parse_last_delivery_at(d.pop("lastDeliveryAt"))

        dead_letter_count = d.pop("deadLetterCount")

        event_subscription = cls(
            event_subscription_id=event_subscription_id,
            url=url,
            event_types=event_types,
            signing_algorithm=signing_algorithm,
            signature_header=signature_header,
            timestamp_header=timestamp_header,
            event_id_header=event_id_header,
            delivery_id_header=delivery_id_header,
            status=status,
            secret_preview=secret_preview,
            created_at=created_at,
            updated_at=updated_at,
            last_delivery_at=last_delivery_at,
            dead_letter_count=dead_letter_count,
        )

        return event_subscription
