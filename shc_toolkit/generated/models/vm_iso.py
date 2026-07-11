from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_iso_available_item import VmIsoAvailableItem
    from ..models.vm_iso_mounted_item import VmIsoMountedItem


T = TypeVar("T", bound="VmIso")


@_attrs_define
class VmIso:
    """ISO images and CD-ROM state for an owned VM.

    Attributes:
        service_id (int): Owned Blesta service id.
        storage (str): Node storage holding ISO images.
        mounted (list[VmIsoMountedItem]): CD-ROM drives currently mounted on the VM.
        available (list[VmIsoAvailableItem]): ISO images available to mount (excludes those already mounted).
        boot_order (list[str]): Current boot order (read-only; changed only via mount/unmount).
    """

    service_id: int
    storage: str
    mounted: list[VmIsoMountedItem]
    available: list[VmIsoAvailableItem]
    boot_order: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        storage = self.storage

        mounted = []
        for mounted_item_data in self.mounted:
            mounted_item = mounted_item_data.to_dict()
            mounted.append(mounted_item)

        available = []
        for available_item_data in self.available:
            available_item = available_item_data.to_dict()
            available.append(available_item)

        boot_order = self.boot_order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "storage": storage,
                "mounted": mounted,
                "available": available,
                "boot_order": boot_order,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_iso_available_item import VmIsoAvailableItem
        from ..models.vm_iso_mounted_item import VmIsoMountedItem

        d = dict(src_dict)
        service_id = d.pop("service_id")

        storage = d.pop("storage")

        mounted = []
        _mounted = d.pop("mounted")
        for mounted_item_data in _mounted:
            mounted_item = VmIsoMountedItem.from_dict(mounted_item_data)

            mounted.append(mounted_item)

        available = []
        _available = d.pop("available")
        for available_item_data in _available:
            available_item = VmIsoAvailableItem.from_dict(available_item_data)

            available.append(available_item)

        boot_order = cast(list[str], d.pop("boot_order"))

        vm_iso = cls(
            service_id=service_id,
            storage=storage,
            mounted=mounted,
            available=available,
            boot_order=boot_order,
        )

        vm_iso.additional_properties = d
        return vm_iso

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
