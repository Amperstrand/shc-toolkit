from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.preview_virtual_machine_term_change_body_additional_property_type_4 import (
        PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4,
    )


T = TypeVar("T", bound="PreviewVirtualMachineTermChangeBody")


@_attrs_define
class PreviewVirtualMachineTermChangeBody:
    """
    Attributes:
        pricing_id (int | str): Required target package_pricing ID for the new term.
    """

    pricing_id: int | str
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.preview_virtual_machine_term_change_body_additional_property_type_4 import (
            PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4,
        )

        pricing_id: int | str
        pricing_id = self.pricing_id

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(
                prop, PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4
            ):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "pricing_id": pricing_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.preview_virtual_machine_term_change_body_additional_property_type_4 import (
            PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4,
        )

        d = dict(src_dict)

        def _parse_pricing_id(data: object) -> int | str:
            return cast(int | str, data)

        pricing_id = _parse_pricing_id(d.pop("pricing_id"))

        preview_virtual_machine_term_change_body = cls(
            pricing_id=pricing_id,
        )

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
                | PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4
                | str
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4.from_dict(
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
                    | PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        preview_virtual_machine_term_change_body.additional_properties = (
            additional_properties
        )
        return preview_virtual_machine_term_change_body

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
        | PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4
        | str
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
        | PreviewVirtualMachineTermChangeBodyAdditionalPropertyType4
        | str,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
