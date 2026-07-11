from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_upgrade_config_option_catalog_values_item import (
        VmUpgradeConfigOptionCatalogValuesItem,
    )


T = TypeVar("T", bound="VmUpgradeConfigOptionCatalog")


@_attrs_define
class VmUpgradeConfigOptionCatalog:
    """A settable/addable config option for an upgradable plan, identical in shape to the ordering catalog (option_id is
    the raw package option id).

        Attributes:
            option_id (int | Unset):  Example: 142.
            name (str | Unset):  Example: disk.
            label (str | Unset):  Example: Disk (GB).
            type_ (str | Unset):  Example: quantity.
            addable (bool | Unset):  Example: True.
            editable (bool | Unset):  Example: True.
            values (list[VmUpgradeConfigOptionCatalogValuesItem] | Unset):
    """

    option_id: int | Unset = UNSET
    name: str | Unset = UNSET
    label: str | Unset = UNSET
    type_: str | Unset = UNSET
    addable: bool | Unset = UNSET
    editable: bool | Unset = UNSET
    values: list[VmUpgradeConfigOptionCatalogValuesItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        option_id = self.option_id

        name = self.name

        label = self.label

        type_ = self.type_

        addable = self.addable

        editable = self.editable

        values: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.values, Unset):
            values = []
            for values_item_data in self.values:
                values_item = values_item_data.to_dict()
                values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if option_id is not UNSET:
            field_dict["option_id"] = option_id
        if name is not UNSET:
            field_dict["name"] = name
        if label is not UNSET:
            field_dict["label"] = label
        if type_ is not UNSET:
            field_dict["type"] = type_
        if addable is not UNSET:
            field_dict["addable"] = addable
        if editable is not UNSET:
            field_dict["editable"] = editable
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_upgrade_config_option_catalog_values_item import (
            VmUpgradeConfigOptionCatalogValuesItem,
        )

        d = dict(src_dict)
        option_id = d.pop("option_id", UNSET)

        name = d.pop("name", UNSET)

        label = d.pop("label", UNSET)

        type_ = d.pop("type", UNSET)

        addable = d.pop("addable", UNSET)

        editable = d.pop("editable", UNSET)

        _values = d.pop("values", UNSET)
        values: list[VmUpgradeConfigOptionCatalogValuesItem] | Unset = UNSET
        if _values is not UNSET:
            values = []
            for values_item_data in _values:
                values_item = VmUpgradeConfigOptionCatalogValuesItem.from_dict(
                    values_item_data
                )

                values.append(values_item)

        vm_upgrade_config_option_catalog = cls(
            option_id=option_id,
            name=name,
            label=label,
            type_=type_,
            addable=addable,
            editable=editable,
            values=values,
        )

        vm_upgrade_config_option_catalog.additional_properties = d
        return vm_upgrade_config_option_catalog

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
