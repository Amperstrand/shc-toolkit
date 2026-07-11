from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmIsoUnmountRequest")


@_attrs_define
class VmIsoUnmountRequest:
    """Unmount a mounted ISO CD-ROM drive. Idempotent: an absent/already-unmounted drive returns 200 with the refreshed
    list.

        Example:
            {'drive': 'ide2'}

        Attributes:
            drive (str): QEMU IDE cdrom drive key to detach (from the `mounted` list of GET /vm/{serviceId}/iso), e.g. ide2.
                Example: ide2.
    """

    drive: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        drive = self.drive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "drive": drive,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        drive = d.pop("drive")

        vm_iso_unmount_request = cls(
            drive=drive,
        )

        vm_iso_unmount_request.additional_properties = d
        return vm_iso_unmount_request

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
