from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.event_subscription_created_delivery_id_header import (
    EventSubscriptionCreatedDeliveryIdHeader,
)
from ..models.event_subscription_created_event_id_header import (
    EventSubscriptionCreatedEventIdHeader,
)
from ..models.event_subscription_created_signature_header import (
    EventSubscriptionCreatedSignatureHeader,
)
from ..models.event_subscription_created_signing_algorithm import (
    EventSubscriptionCreatedSigningAlgorithm,
)
from ..models.event_subscription_created_status import EventSubscriptionCreatedStatus
from ..models.event_subscription_created_timestamp_header import (
    EventSubscriptionCreatedTimestampHeader,
)

T = TypeVar("T", bound="EventSubscriptionCreated")


@_attrs_define
class EventSubscriptionCreated:
    """Create response body for a new webhook subscription. Includes the one-time signing secret.

    Attributes:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.
        url (str): Registered HTTPS webhook destination. Example: https://hooks.customer-domain.com/shc/webhooks.
        event_types (list[str]): CloudEvents type filters matched against the customer-scoped /events feed.
        signing_algorithm (EventSubscriptionCreatedSigningAlgorithm):  Example: HMAC-SHA256.
        signature_header (EventSubscriptionCreatedSignatureHeader):  Example: X-SHC-Webhook-Signature.
        timestamp_header (EventSubscriptionCreatedTimestampHeader):  Example: X-SHC-Webhook-Timestamp.
        event_id_header (EventSubscriptionCreatedEventIdHeader):  Example: X-SHC-Webhook-Event-Id.
        delivery_id_header (EventSubscriptionCreatedDeliveryIdHeader):  Example: X-SHC-Webhook-Delivery-Id.
        status (EventSubscriptionCreatedStatus):  Example: active.
        secret_preview (str): Display-only prefix. It is not enough to verify signatures. Example: whsec_abc123....
        created_at (datetime.datetime):  Example: 2026-07-13T22:30:00Z.
        updated_at (datetime.datetime):  Example: 2026-07-13T22:30:00Z.
        last_delivery_at (datetime.datetime | None):  Example: 2026-07-13T22:31:00Z.
        dead_letter_count (int):
        secret (str): Server-generated HMAC signing secret. Returned once in the initial 201 create response; store it
            immediately. It is omitted from 200 idempotent replay responses. Example:
            whsec_0123456789abcdef0123456789abcdef0123456789ab.
    """

    event_subscription_id: str
    url: str
    event_types: list[str]
    signing_algorithm: EventSubscriptionCreatedSigningAlgorithm
    signature_header: EventSubscriptionCreatedSignatureHeader
    timestamp_header: EventSubscriptionCreatedTimestampHeader
    event_id_header: EventSubscriptionCreatedEventIdHeader
    delivery_id_header: EventSubscriptionCreatedDeliveryIdHeader
    status: EventSubscriptionCreatedStatus
    secret_preview: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_delivery_at: datetime.datetime | None
    dead_letter_count: int
    secret: str

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

        secret = self.secret

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
                "secret": secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        event_subscription_id = d.pop("eventSubscriptionId")

        url = d.pop("url")

        event_types = cast(list[str], d.pop("eventTypes"))

        signing_algorithm = EventSubscriptionCreatedSigningAlgorithm(
            d.pop("signingAlgorithm")
        )

        signature_header = EventSubscriptionCreatedSignatureHeader(
            d.pop("signatureHeader")
        )

        timestamp_header = EventSubscriptionCreatedTimestampHeader(
            d.pop("timestampHeader")
        )

        event_id_header = EventSubscriptionCreatedEventIdHeader(d.pop("eventIdHeader"))

        delivery_id_header = EventSubscriptionCreatedDeliveryIdHeader(
            d.pop("deliveryIdHeader")
        )

        status = EventSubscriptionCreatedStatus(d.pop("status"))

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

        secret = d.pop("secret")

        event_subscription_created = cls(
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
            secret=secret,
        )

        return event_subscription_created
