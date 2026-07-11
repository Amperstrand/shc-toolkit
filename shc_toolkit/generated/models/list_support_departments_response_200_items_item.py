from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.list_support_departments_response_200_items_item_default_priority import (
    ListSupportDepartmentsResponse200ItemsItemDefaultPriority,
)
from ..models.list_support_departments_response_200_items_item_priorities_item import (
    ListSupportDepartmentsResponse200ItemsItemPrioritiesItem,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_support_departments_response_200_items_item_fields_item import (
        ListSupportDepartmentsResponse200ItemsItemFieldsItem,
    )


T = TypeVar("T", bound="ListSupportDepartmentsResponse200ItemsItem")


@_attrs_define
class ListSupportDepartmentsResponse200ItemsItem:
    """
    Attributes:
        id (int):  Example: 3.
        name (str):  Example: Technical Support.
        default_priority (ListSupportDepartmentsResponse200ItemsItemDefaultPriority):  Example: medium.
        clients_only (bool):  Example: True.
        priorities (list[ListSupportDepartmentsResponse200ItemsItemPrioritiesItem]):
        fields (list[ListSupportDepartmentsResponse200ItemsItemFieldsItem]):
        description (None | str | Unset):
    """

    id: int
    name: str
    default_priority: ListSupportDepartmentsResponse200ItemsItemDefaultPriority
    clients_only: bool
    priorities: list[ListSupportDepartmentsResponse200ItemsItemPrioritiesItem]
    fields: list[ListSupportDepartmentsResponse200ItemsItemFieldsItem]
    description: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        default_priority = self.default_priority.value

        clients_only = self.clients_only

        priorities = []
        for priorities_item_data in self.priorities:
            priorities_item = priorities_item_data.value
            priorities.append(priorities_item)

        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()
            fields.append(fields_item)

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
                "default_priority": default_priority,
                "clients_only": clients_only,
                "priorities": priorities,
                "fields": fields,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_support_departments_response_200_items_item_fields_item import (
            ListSupportDepartmentsResponse200ItemsItemFieldsItem,
        )

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        default_priority = ListSupportDepartmentsResponse200ItemsItemDefaultPriority(
            d.pop("default_priority")
        )

        clients_only = d.pop("clients_only")

        priorities = []
        _priorities = d.pop("priorities")
        for priorities_item_data in _priorities:
            priorities_item = ListSupportDepartmentsResponse200ItemsItemPrioritiesItem(
                priorities_item_data
            )

            priorities.append(priorities_item)

        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = (
                ListSupportDepartmentsResponse200ItemsItemFieldsItem.from_dict(
                    fields_item_data
                )
            )

            fields.append(fields_item)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        list_support_departments_response_200_items_item = cls(
            id=id,
            name=name,
            default_priority=default_priority,
            clients_only=clients_only,
            priorities=priorities,
            fields=fields,
            description=description,
        )

        return list_support_departments_response_200_items_item
