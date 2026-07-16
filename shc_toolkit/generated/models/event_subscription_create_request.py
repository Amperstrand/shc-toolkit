from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="EventSubscriptionCreateRequest")


@_attrs_define
class EventSubscriptionCreateRequest:
    """Register an asynchronous webhook subscription for the existing customer event feed. The signing secret is generated
    by the server and returned only in the first 201 response, never in replay or read responses.

        Example:
            {'url': 'https://hooks.customer-domain.com/shc/webhooks', 'eventTypes': ['service.lifecycle.*',
                'billing.invoice.*']}

        Attributes:
            url (str): HTTPS webhook destination. The server accepts only standard-port HTTPS URLs whose host resolves to
                public IP addresses. Registration and every delivery reject loopback, link-local, private, metadata, .local,
                non-HTTPS, non-standard-port, and DNS-rebound targets. Example: https://hooks.customer-domain.com/shc/webhooks.
            event_types (list[str]): CloudEvents type filters matched against the customer-scoped /events feed.
    """

    url: str
    event_types: list[str]

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        event_types = self.event_types

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
                "eventTypes": event_types,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        event_types = cast(list[str], d.pop("eventTypes"))

        event_subscription_create_request = cls(
            url=url,
            event_types=event_types,
        )

        return event_subscription_create_request
