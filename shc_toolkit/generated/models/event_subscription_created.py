from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.event_subscription_created_delivery_id_header import (
    EventSubscriptionCreatedDeliveryIdHeader,
    check_event_subscription_created_delivery_id_header,
)
from ..models.event_subscription_created_event_id_header import (
    EventSubscriptionCreatedEventIdHeader,
    check_event_subscription_created_event_id_header,
)
from ..models.event_subscription_created_signature_header import (
    EventSubscriptionCreatedSignatureHeader,
    check_event_subscription_created_signature_header,
)
from ..models.event_subscription_created_signing_algorithm import (
    EventSubscriptionCreatedSigningAlgorithm,
    check_event_subscription_created_signing_algorithm,
)
from ..models.event_subscription_created_status import (
    EventSubscriptionCreatedStatus,
    check_event_subscription_created_status,
)
from ..models.event_subscription_created_timestamp_header import (
    EventSubscriptionCreatedTimestampHeader,
    check_event_subscription_created_timestamp_header,
)

T = TypeVar("T", bound="EventSubscriptionCreated")


@_attrs_define
class EventSubscriptionCreated:
    """Create response body for a new webhook subscription. Includes the one-time signing secret."""

    event_subscription_id: str
    url: str
    """ Registered HTTPS webhook destination. """
    event_types: list[str]
    """ CloudEvents type filters matched against the customer-scoped /events feed. """
    signing_algorithm: EventSubscriptionCreatedSigningAlgorithm
    signature_header: EventSubscriptionCreatedSignatureHeader
    timestamp_header: EventSubscriptionCreatedTimestampHeader
    event_id_header: EventSubscriptionCreatedEventIdHeader
    delivery_id_header: EventSubscriptionCreatedDeliveryIdHeader
    status: EventSubscriptionCreatedStatus
    secret_preview: str
    """ Display-only prefix. It is not enough to verify signatures. """
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_delivery_at: datetime.datetime | None
    dead_letter_count: int
    secret: str
    """ Server-generated HMAC signing secret. Returned once in the initial 201 create response; store it
    immediately. It is omitted from 200 idempotent replay responses. """

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        event_subscription_id = d.pop("eventSubscriptionId")

        url = d.pop("url")

        event_types = cast(list[str], d.pop("eventTypes"))

        signing_algorithm = check_event_subscription_created_signing_algorithm(
            d.pop("signingAlgorithm")
        )

        signature_header = check_event_subscription_created_signature_header(
            d.pop("signatureHeader")
        )

        timestamp_header = check_event_subscription_created_timestamp_header(
            d.pop("timestampHeader")
        )

        event_id_header = check_event_subscription_created_event_id_header(
            d.pop("eventIdHeader")
        )

        delivery_id_header = check_event_subscription_created_delivery_id_header(
            d.pop("deliveryIdHeader")
        )

        status = check_event_subscription_created_status(d.pop("status"))

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
