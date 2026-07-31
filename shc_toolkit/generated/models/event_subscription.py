from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.event_subscription_delivery_id_header import (
    EventSubscriptionDeliveryIdHeader,
    check_event_subscription_delivery_id_header,
)
from ..models.event_subscription_event_id_header import (
    EventSubscriptionEventIdHeader,
    check_event_subscription_event_id_header,
)
from ..models.event_subscription_signature_header import (
    EventSubscriptionSignatureHeader,
    check_event_subscription_signature_header,
)
from ..models.event_subscription_signing_algorithm import (
    EventSubscriptionSigningAlgorithm,
    check_event_subscription_signing_algorithm,
)
from ..models.event_subscription_status import (
    EventSubscriptionStatus,
    check_event_subscription_status,
)
from ..models.event_subscription_timestamp_header import (
    EventSubscriptionTimestampHeader,
    check_event_subscription_timestamp_header,
)

T = TypeVar("T", bound="EventSubscription")


@_attrs_define
class EventSubscription:
    """Webhook subscription metadata. The signing secret is not present on read, list, delete, or idempotent replay
    responses.

    """

    event_subscription_id: str
    url: str
    """ Registered HTTPS webhook destination. """
    event_types: list[str]
    """ CloudEvents type filters matched against the customer-scoped /events feed. """
    signing_algorithm: EventSubscriptionSigningAlgorithm
    signature_header: EventSubscriptionSignatureHeader
    timestamp_header: EventSubscriptionTimestampHeader
    event_id_header: EventSubscriptionEventIdHeader
    delivery_id_header: EventSubscriptionDeliveryIdHeader
    status: EventSubscriptionStatus
    secret_preview: str
    """ Display-only prefix. It is not enough to verify signatures. """
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_delivery_at: datetime.datetime | None
    dead_letter_count: int

    def to_dict(self) -> dict[str, Any]:
        event_subscription_id = self.event_subscription_id

        url = self.url

        event_types = self.event_types

        signing_algorithm: str = self.signing_algorithm

        signature_header: str = self.signature_header

        timestamp_header: str = self.timestamp_header

        event_id_header: str = self.event_id_header

        delivery_id_header: str = self.delivery_id_header

        status: str = self.status

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        event_subscription_id = d.pop("eventSubscriptionId")

        url = d.pop("url")

        event_types = cast(list[str], d.pop("eventTypes"))

        signing_algorithm = check_event_subscription_signing_algorithm(
            d.pop("signingAlgorithm")
        )

        signature_header = check_event_subscription_signature_header(
            d.pop("signatureHeader")
        )

        timestamp_header = check_event_subscription_timestamp_header(
            d.pop("timestampHeader")
        )

        event_id_header = check_event_subscription_event_id_header(
            d.pop("eventIdHeader")
        )

        delivery_id_header = check_event_subscription_delivery_id_header(
            d.pop("deliveryIdHeader")
        )

        status = check_event_subscription_status(d.pop("status"))

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
