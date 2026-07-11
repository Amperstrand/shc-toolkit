from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmIsoMountRequest")


@_attrs_define
class VmIsoMountRequest:
    """Mount an ISO image as a new CD-ROM drive. The ISO must be one offered by GET /vm/{serviceId}/iso and not already
    mounted.

        Example:
            {'iso': 'local:iso/debian-12.7.0-amd64-netinst.iso'}

        Attributes:
            iso (str): Proxmox volume id of the ISO to mount (from the `available` list of GET /vm/{serviceId}/iso).
                Example: local:iso/debian-12.7.0-amd64-netinst.iso.
    """

    iso: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        iso = self.iso

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "iso": iso,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        iso = d.pop("iso")

        vm_iso_mount_request = cls(
            iso=iso,
        )

        vm_iso_mount_request.additional_properties = d
        return vm_iso_mount_request

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
