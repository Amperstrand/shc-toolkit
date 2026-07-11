from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.pagination import Pagination
    from ..models.plan import Plan


T = TypeVar("T", bound="PlanList")


@_attrs_define
class PlanList:
    """Canonical paginated list of descriptive VM plans. Each item embeds its default image metadata when available.

    Attributes:
        items (list[Plan]):
        pagination (Pagination):  Example: {'total': 42, 'limit': 100, 'offset': 0, 'has_more': False}.
    """

    items: list[Plan]
    pagination: Pagination

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        pagination = self.pagination.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "items": items,
                "pagination": pagination,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pagination import Pagination
        from ..models.plan import Plan

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = Plan.from_dict(items_item_data)

            items.append(items_item)

        pagination = Pagination.from_dict(d.pop("pagination"))

        plan_list = cls(
            items=items,
            pagination=pagination,
        )

        return plan_list
