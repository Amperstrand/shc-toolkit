from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.reinstall_vm_request_additional_property_type_4 import (
        ReinstallVmRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="ReinstallVmRequest")


@_attrs_define
class ReinstallVmRequest:
    """
    Example:
        {'template': 'debian13-cloud'}

    Attributes:
        template (str): Machine-stable OS template identifier to reinstall onto the VM. Must be one the customer's plan
            offers in the live /ordering/catalog `template` option (e.g. debian13-cloud, debian12-cloud, ubuntu2404-cloud,
            ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud, alpine323-cloud, devuan5-cloud,
            openbsd79-cloud, windows2022-byol). Example: debian13-cloud.
    """

    template: str
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | ReinstallVmRequestAdditionalPropertyType4
        | str,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.reinstall_vm_request_additional_property_type_4 import (
            ReinstallVmRequestAdditionalPropertyType4,
        )

        template = self.template

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, ReinstallVmRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "template": template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reinstall_vm_request_additional_property_type_4 import (
            ReinstallVmRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        template = d.pop("template")

        reinstall_vm_request = cls(
            template=template,
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
                | ReinstallVmRequestAdditionalPropertyType4
                | str
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        ReinstallVmRequestAdditionalPropertyType4.from_dict(data)
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
                    | ReinstallVmRequestAdditionalPropertyType4
                    | str,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        reinstall_vm_request.additional_properties = additional_properties
        return reinstall_vm_request

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
        | ReinstallVmRequestAdditionalPropertyType4
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
        | ReinstallVmRequestAdditionalPropertyType4
        | str,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
