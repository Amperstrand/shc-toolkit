from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListVmFileRestoreEntriesResponse200DataEntriesItem")


@_attrs_define
class ListVmFileRestoreEntriesResponse200DataEntriesItem:
    """
    Attributes:
        filepath (str):
        text (str):
        leaf (bool):
        type_ (None | str | Unset):
        size (int | None | Unset):
    """

    filepath: str
    text: str
    leaf: bool
    type_: None | str | Unset = UNSET
    size: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filepath = self.filepath

        text = self.text

        leaf = self.leaf

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        size: int | None | Unset
        if isinstance(self.size, Unset):
            size = UNSET
        else:
            size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filepath": filepath,
                "text": text,
                "leaf": leaf,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filepath = d.pop("filepath")

        text = d.pop("text")

        leaf = d.pop("leaf")

        def _parse_type_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size = _parse_size(d.pop("size", UNSET))

        list_vm_file_restore_entries_response_200_data_entries_item = cls(
            filepath=filepath,
            text=text,
            leaf=leaf,
            type_=type_,
            size=size,
        )

        list_vm_file_restore_entries_response_200_data_entries_item.additional_properties = d
        return list_vm_file_restore_entries_response_200_data_entries_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
