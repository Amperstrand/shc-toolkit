from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_upgrade_config_option_catalog_values_item_additional_property_type_4 import (
        VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4,
    )


T = TypeVar("T", bound="VmUpgradeConfigOptionCatalogValuesItem")


@_attrs_define
class VmUpgradeConfigOptionCatalogValuesItem:
    """ """

    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_upgrade_config_option_catalog_values_item_additional_property_type_4 import (
            VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(
                prop, VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4
            ):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_upgrade_config_option_catalog_values_item_additional_property_type_4 import (
            VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4,
        )

        d = dict(src_dict)
        vm_upgrade_config_option_catalog_values_item = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                bool
                | float
                | int
                | list[str]
                | None
                | str
                | VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4.from_dict(
                        data
                    )

                    return additional_property_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_5 = cast(list[str], data)

                    return additional_property_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(
                    bool
                    | float
                    | int
                    | list[str]
                    | None
                    | str
                    | VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_upgrade_config_option_catalog_values_item.additional_properties = (
            additional_properties
        )
        return vm_upgrade_config_option_catalog_values_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4
    ):
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmUpgradeConfigOptionCatalogValuesItemAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
