from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmIsoMountedItem")


@_attrs_define
class VmIsoMountedItem:
    """
    Attributes:
        drive (str): QEMU drive key (e.g. ide2).
        volid (str): Proxmox volume id of the mounted ISO.
    """

    drive: str
    volid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        drive = self.drive

        volid = self.volid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "drive": drive,
                "volid": volid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        drive = d.pop("drive")

        volid = d.pop("volid")

        vm_iso_mounted_item = cls(
            drive=drive,
            volid=volid,
        )

        vm_iso_mounted_item.additional_properties = d
        return vm_iso_mounted_item

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
