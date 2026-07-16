from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.cloud_event import CloudEvent
    from ..models.links import Links


T = TypeVar("T", bound="ListEventsResponse200")


@_attrs_define
class ListEventsResponse200:
    """
    Attributes:
        items (list[CloudEvent]):
        next_cursor (None | str):  Example: evt_01J2Z7QCGJ7FQ86A6W6A9A0M5X.
        links (Links): Hypermedia links keyed by IANA-registered link relation names.
    """

    items: list[CloudEvent]
    next_cursor: None | str
    links: Links

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        links = self.links.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "items": items,
                "nextCursor": next_cursor,
                "links": links,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_event import CloudEvent
        from ..models.links import Links

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = CloudEvent.from_dict(items_item_data)

            items.append(items_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))

        links = Links.from_dict(d.pop("links"))

        list_events_response_200 = cls(
            items=items,
            next_cursor=next_cursor,
            links=links,
        )

        return list_events_response_200
