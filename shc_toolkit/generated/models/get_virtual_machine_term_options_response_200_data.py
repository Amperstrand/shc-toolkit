from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.get_virtual_machine_term_options_response_200_data_items_item import (
        GetVirtualMachineTermOptionsResponse200DataItemsItem,
    )


T = TypeVar("T", bound="GetVirtualMachineTermOptionsResponse200Data")


@_attrs_define
class GetVirtualMachineTermOptionsResponse200Data:
    service_id: int
    term_change_allowed: bool
    """ Whether this client is allowed to change service term. """
    items: list[GetVirtualMachineTermOptionsResponse200DataItemsItem]
    """ Available recurring terms for the service package. """

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        term_change_allowed = self.term_change_allowed

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "term_change_allowed": term_change_allowed,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_virtual_machine_term_options_response_200_data_items_item import (
            GetVirtualMachineTermOptionsResponse200DataItemsItem,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        term_change_allowed = d.pop("term_change_allowed")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = GetVirtualMachineTermOptionsResponse200DataItemsItem.from_dict(
                items_item_data
            )

            items.append(items_item)

        get_virtual_machine_term_options_response_200_data = cls(
            service_id=service_id,
            term_change_allowed=term_change_allowed,
            items=items,
        )

        return get_virtual_machine_term_options_response_200_data
