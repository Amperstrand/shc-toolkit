from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.event_subscription_created import EventSubscriptionCreated


T = TypeVar("T", bound="CreateEventSubscriptionResponse201")


@_attrs_define
class CreateEventSubscriptionResponse201:
    """
    Attributes:
        data (EventSubscriptionCreated): Create response body for a new webhook subscription. Includes the one-time
            signing secret.
    """

    data: EventSubscriptionCreated

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
        from ..models.event_subscription_created import EventSubscriptionCreated

        d = dict(src_dict)
        data = EventSubscriptionCreated.from_dict(d.pop("data"))

        create_event_subscription_response_201 = cls(
            data=data,
        )

        return create_event_subscription_response_201
