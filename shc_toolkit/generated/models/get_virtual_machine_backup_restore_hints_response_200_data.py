from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_virtual_machine_backup_restore_hints_response_200_data_source import (
    GetVirtualMachineBackupRestoreHintsResponse200DataSource,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_virtual_machine_backup_restore_hints_response_200_data_unwrap_hints_item import (
        GetVirtualMachineBackupRestoreHintsResponse200DataUnwrapHintsItem,
    )


T = TypeVar("T", bound="GetVirtualMachineBackupRestoreHintsResponse200Data")


@_attrs_define
class GetVirtualMachineBackupRestoreHintsResponse200Data:
    """
    Attributes:
        service_id (int):
        source (GetVirtualMachineBackupRestoreHintsResponse200DataSource):
        backup_id (str): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the real
            storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side. Example: bk_6ERwSd_PLY66FW72VFM.
        encrypted (bool):
        key_type (str | Unset):
        wrapped_blob (str | Unset):
        unwrap_hints (list[GetVirtualMachineBackupRestoreHintsResponse200DataUnwrapHintsItem] | Unset):
        fingerprint (str | Unset):
    """

    service_id: int
    source: GetVirtualMachineBackupRestoreHintsResponse200DataSource
    backup_id: str
    encrypted: bool
    key_type: str | Unset = UNSET
    wrapped_blob: str | Unset = UNSET
    unwrap_hints: (
        list[GetVirtualMachineBackupRestoreHintsResponse200DataUnwrapHintsItem] | Unset
    ) = UNSET
    fingerprint: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        source = self.source.value

        backup_id = self.backup_id

        encrypted = self.encrypted

        key_type = self.key_type

        wrapped_blob = self.wrapped_blob

        unwrap_hints: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.unwrap_hints, Unset):
            unwrap_hints = []
            for unwrap_hints_item_data in self.unwrap_hints:
                unwrap_hints_item = unwrap_hints_item_data.to_dict()
                unwrap_hints.append(unwrap_hints_item)

        fingerprint = self.fingerprint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "source": source,
                "backup_id": backup_id,
                "encrypted": encrypted,
            }
        )
        if key_type is not UNSET:
            field_dict["key_type"] = key_type
        if wrapped_blob is not UNSET:
            field_dict["wrapped_blob"] = wrapped_blob
        if unwrap_hints is not UNSET:
            field_dict["unwrap_hints"] = unwrap_hints
        if fingerprint is not UNSET:
            field_dict["fingerprint"] = fingerprint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_virtual_machine_backup_restore_hints_response_200_data_unwrap_hints_item import (
            GetVirtualMachineBackupRestoreHintsResponse200DataUnwrapHintsItem,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        source = GetVirtualMachineBackupRestoreHintsResponse200DataSource(
            d.pop("source")
        )

        backup_id = d.pop("backup_id")

        encrypted = d.pop("encrypted")

        key_type = d.pop("key_type", UNSET)

        wrapped_blob = d.pop("wrapped_blob", UNSET)

        _unwrap_hints = d.pop("unwrap_hints", UNSET)
        unwrap_hints: (
            list[GetVirtualMachineBackupRestoreHintsResponse200DataUnwrapHintsItem]
            | Unset
        ) = UNSET
        if _unwrap_hints is not UNSET:
            unwrap_hints = []
            for unwrap_hints_item_data in _unwrap_hints:
                unwrap_hints_item = GetVirtualMachineBackupRestoreHintsResponse200DataUnwrapHintsItem.from_dict(
                    unwrap_hints_item_data
                )

                unwrap_hints.append(unwrap_hints_item)

        fingerprint = d.pop("fingerprint", UNSET)

        get_virtual_machine_backup_restore_hints_response_200_data = cls(
            service_id=service_id,
            source=source,
            backup_id=backup_id,
            encrypted=encrypted,
            key_type=key_type,
            wrapped_blob=wrapped_blob,
            unwrap_hints=unwrap_hints,
            fingerprint=fingerprint,
        )

        get_virtual_machine_backup_restore_hints_response_200_data.additional_properties = d
        return get_virtual_machine_backup_restore_hints_response_200_data

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
