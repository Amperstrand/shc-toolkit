from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_iso_mount_request_additional_property_type_4 import (
        VmIsoMountRequestAdditionalPropertyType4,
    )


T = TypeVar("T", bound="VmIsoMountRequest")


@_attrs_define
class VmIsoMountRequest:
    """Mount an ISO image as a new CD-ROM drive. The ISO must be one offered by GET /vm/{service_id}/iso and not already
    mounted.

        Example:
            {'iso': 'local:iso/debian-12.7.0-amd64-netinst.iso'}

        Attributes:
            iso (str): Proxmox volume id of the ISO to mount (from the `available` list of GET /vm/{service_id}/iso).
                Example: local:iso/debian-12.7.0-amd64-netinst.iso.
    """

    iso: str
    additional_properties: dict[
        str,
        bool
        | float
        | int
        | list[str]
        | None
        | str
        | VmIsoMountRequestAdditionalPropertyType4,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_iso_mount_request_additional_property_type_4 import (
            VmIsoMountRequestAdditionalPropertyType4,
        )

        iso = self.iso

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, VmIsoMountRequestAdditionalPropertyType4):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update(
            {
                "iso": iso,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_iso_mount_request_additional_property_type_4 import (
            VmIsoMountRequestAdditionalPropertyType4,
        )

        d = dict(src_dict)
        iso = d.pop("iso")

        vm_iso_mount_request = cls(
            iso=iso,
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
                | str
                | VmIsoMountRequestAdditionalPropertyType4
            ):
                if data is None:
                    return data
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_4 = (
                        VmIsoMountRequestAdditionalPropertyType4.from_dict(data)
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
                    | VmIsoMountRequestAdditionalPropertyType4,
                    data,
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        vm_iso_mount_request.additional_properties = additional_properties
        return vm_iso_mount_request

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
        | VmIsoMountRequestAdditionalPropertyType4
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
        | VmIsoMountRequestAdditionalPropertyType4,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
