from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_upgradable_plan_available_config_options_item_additional_property_type_4 import (
        VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4,
    )


T = TypeVar("T", bound="VmUpgradablePlanAvailableConfigOptionsItem")


@_attrs_define
class VmUpgradablePlanAvailableConfigOptionsItem:
    """ """

    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_upgradable_plan_available_config_options_item_additional_property_type_4 import (
            VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(
                prop, VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4
            ):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_upgradable_plan_available_config_options_item_additional_property_type_4 import (
            VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4,
        )

        d = dict(src_dict)
        vm_upgradable_plan_available_config_options_item = cls()

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
                | VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4.from_dict(
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
                    | VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_upgradable_plan_available_config_options_item.additional_properties = (
            additional_properties
        )
        return vm_upgradable_plan_available_config_options_item

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
        | VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4
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
        | VmUpgradablePlanAvailableConfigOptionsItemAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
