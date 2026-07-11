from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.list_support_departments_response_200_items_item_fields_item_type import (
    ListSupportDepartmentsResponse200ItemsItemFieldsItemType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListSupportDepartmentsResponse200ItemsItemFieldsItem")


@_attrs_define
class ListSupportDepartmentsResponse200ItemsItemFieldsItem:
    """
    Attributes:
        id (int):  Example: 12.
        label (str):  Example: Affected service.
        type_ (ListSupportDepartmentsResponse200ItemsItemFieldsItemType):  Example: text.
        required (bool):
        description (None | str | Unset):
        options (list[str] | None | str | Unset): Field options (array for select/radio/checkbox; otherwise null or raw
            string).
    """

    id: int
    label: str
    type_: ListSupportDepartmentsResponse200ItemsItemFieldsItemType
    required: bool
    description: None | str | Unset = UNSET
    options: list[str] | None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        label = self.label

        type_ = self.type_.value

        required = self.required

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        options: list[str] | None | str | Unset
        if isinstance(self.options, Unset):
            options = UNSET
        elif isinstance(self.options, list):
            options = self.options

        else:
            options = self.options

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "label": label,
                "type": type_,
                "required": required,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        label = d.pop("label")

        type_ = ListSupportDepartmentsResponse200ItemsItemFieldsItemType(d.pop("type"))

        required = d.pop("required")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_options(data: object) -> list[str] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                options_type_0 = cast(list[str], data)

                return options_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | str | Unset, data)

        options = _parse_options(d.pop("options", UNSET))

        list_support_departments_response_200_items_item_fields_item = cls(
            id=id,
            label=label,
            type_=type_,
            required=required,
            description=description,
            options=options,
        )

        return list_support_departments_response_200_items_item_fields_item
