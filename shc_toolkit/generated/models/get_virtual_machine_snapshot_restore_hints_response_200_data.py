from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_virtual_machine_snapshot_restore_hints_response_200_data_source import (
    GetVirtualMachineSnapshotRestoreHintsResponse200DataSource,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_virtual_machine_snapshot_restore_hints_response_200_data_unwrap_hints_item_type_4 import (
        GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4,
    )


T = TypeVar("T", bound="GetVirtualMachineSnapshotRestoreHintsResponse200Data")


@_attrs_define
class GetVirtualMachineSnapshotRestoreHintsResponse200Data:
    """
    Attributes:
        service_id (int):
        source (GetVirtualMachineSnapshotRestoreHintsResponse200DataSource):
        backup_id (str): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the real
            storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side. Example: bk_6ERwSd_PLY66FW72VFM.
        encrypted (bool):
        key_type (str | Unset):
        wrapped_blob (str | Unset):
        unwrap_hints (list[bool | float | GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4 | int
            | list[str] | None | str] | Unset):
        fingerprint (str | Unset):
    """

    service_id: int
    source: GetVirtualMachineSnapshotRestoreHintsResponse200DataSource
    backup_id: str
    encrypted: bool
    key_type: str | Unset = UNSET
    wrapped_blob: str | Unset = UNSET
    unwrap_hints: (
        list[
            bool
            | float
            | GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4
            | int
            | list[str]
            | None
            | str
        ]
        | Unset
    ) = UNSET
    fingerprint: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.get_virtual_machine_snapshot_restore_hints_response_200_data_unwrap_hints_item_type_4 import (
            GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4,
        )

        service_id = self.service_id

        source = self.source.value

        backup_id = self.backup_id

        encrypted = self.encrypted

        key_type = self.key_type

        wrapped_blob = self.wrapped_blob

        unwrap_hints: (
            list[bool | dict[str, Any] | float | int | list[str] | None | str] | Unset
        ) = UNSET
        if not isinstance(self.unwrap_hints, Unset):
            unwrap_hints = []
            for unwrap_hints_item_data in self.unwrap_hints:
                unwrap_hints_item: (
                    bool | dict[str, Any] | float | int | list[str] | None | str
                )
                if isinstance(
                    unwrap_hints_item_data,
                    GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4,
                ):
                    unwrap_hints_item = unwrap_hints_item_data.to_dict()
                elif isinstance(unwrap_hints_item_data, list):
                    unwrap_hints_item = unwrap_hints_item_data

                else:
                    unwrap_hints_item = unwrap_hints_item_data
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
        from ..models.get_virtual_machine_snapshot_restore_hints_response_200_data_unwrap_hints_item_type_4 import (
            GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        source = GetVirtualMachineSnapshotRestoreHintsResponse200DataSource(
            d.pop("source")
        )

        backup_id = d.pop("backup_id")

        encrypted = d.pop("encrypted")

        key_type = d.pop("key_type", UNSET)

        wrapped_blob = d.pop("wrapped_blob", UNSET)

        _unwrap_hints = d.pop("unwrap_hints", UNSET)
        unwrap_hints: (
            list[
                bool
                | float
                | GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4
                | int
                | list[str]
                | None
                | str
            ]
            | Unset
        ) = UNSET
        if _unwrap_hints is not UNSET:
            unwrap_hints = []
            for unwrap_hints_item_data in _unwrap_hints:

                def _parse_unwrap_hints_item(
                    data: object,
                ) -> (
                    bool
                    | float
                    | GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4
                    | int
                    | list[str]
                    | None
                    | str
                ):
                    if data is None:
                        return data
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        unwrap_hints_item_type_4 = GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4.from_dict(
                            data
                        )

                        return unwrap_hints_item_type_4
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, list):
                            raise TypeError()
                        unwrap_hints_item_type_5 = cast(list[str], data)

                        return unwrap_hints_item_type_5
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    return cast(
                        bool
                        | float
                        | GetVirtualMachineSnapshotRestoreHintsResponse200DataUnwrapHintsItemType4
                        | int
                        | list[str]
                        | None
                        | str,
                        data,
                    )

                unwrap_hints_item = _parse_unwrap_hints_item(unwrap_hints_item_data)

                unwrap_hints.append(unwrap_hints_item)

        fingerprint = d.pop("fingerprint", UNSET)

        get_virtual_machine_snapshot_restore_hints_response_200_data = cls(
            service_id=service_id,
            source=source,
            backup_id=backup_id,
            encrypted=encrypted,
            key_type=key_type,
            wrapped_blob=wrapped_blob,
            unwrap_hints=unwrap_hints,
            fingerprint=fingerprint,
        )

        get_virtual_machine_snapshot_restore_hints_response_200_data.additional_properties = d
        return get_virtual_machine_snapshot_restore_hints_response_200_data

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
