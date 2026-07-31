from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.pagination import Pagination
    from ..models.vm_activity_item import VmActivityItem


T = TypeVar("T", bound="ListVirtualMachineActivityResponse200")


@_attrs_define
class ListVirtualMachineActivityResponse200:
    items: list[VmActivityItem]
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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.pagination import Pagination
        from ..models.vm_activity_item import VmActivityItem

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = VmActivityItem.from_dict(items_item_data)

            items.append(items_item)

        pagination = Pagination.from_dict(d.pop("pagination"))

        list_virtual_machine_activity_response_200 = cls(
            items=items,
            pagination=pagination,
        )

        return list_virtual_machine_activity_response_200
