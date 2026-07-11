from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmStorageVerifyResponse")


@_attrs_define
class VmStorageVerifyResponse:
    """Synchronous no-op verify acknowledgement (no background job is queued).

    Attributes:
        service_id (int):  Example: 353.
        acknowledged (bool):  Example: True.
        backup_id (str): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the real
            storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side. Example: bk_6ERwSd_PLY66FW72VFM.
    """

    service_id: int
    acknowledged: bool
    backup_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        acknowledged = self.acknowledged

        backup_id = self.backup_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "acknowledged": acknowledged,
                "backup_id": backup_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        acknowledged = d.pop("acknowledged")

        backup_id = d.pop("backup_id")

        vm_storage_verify_response = cls(
            service_id=service_id,
            acknowledged=acknowledged,
            backup_id=backup_id,
        )

        vm_storage_verify_response.additional_properties = d
        return vm_storage_verify_response

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
