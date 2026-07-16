from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.event_subscription import EventSubscription


T = TypeVar("T", bound="CreateEventSubscriptionResponse200")


@_attrs_define
class CreateEventSubscriptionResponse200:
    """
    Attributes:
        data (EventSubscription): Webhook subscription metadata. The signing secret is not present on read, list,
            delete, or idempotent replay responses.
    """

    data: EventSubscription

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.event_subscription import EventSubscription

        d = dict(src_dict)
        data = EventSubscription.from_dict(d.pop("data"))

        create_event_subscription_response_200 = cls(
            data=data,
        )

        return create_event_subscription_response_200
