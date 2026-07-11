from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_vm_file_restore_entries_response_200_data_entries_item import (
        ListVmFileRestoreEntriesResponse200DataEntriesItem,
    )


T = TypeVar("T", bound="ListVmFileRestoreEntriesResponse200Data")


@_attrs_define
class ListVmFileRestoreEntriesResponse200Data:
    """
    Attributes:
        service_id (int):
        backup_id (str): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the real
            storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side. Example: bk_6ERwSd_PLY66FW72VFM.
        storage (str):
        path (str):
        entries (list[ListVmFileRestoreEntriesResponse200DataEntriesItem]):
        base (None | str | Unset):
    """

    service_id: int
    backup_id: str
    storage: str
    path: str
    entries: list[ListVmFileRestoreEntriesResponse200DataEntriesItem]
    base: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        backup_id = self.backup_id

        storage = self.storage

        path = self.path

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        base: None | str | Unset
        if isinstance(self.base, Unset):
            base = UNSET
        else:
            base = self.base

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "backup_id": backup_id,
                "storage": storage,
                "path": path,
                "entries": entries,
            }
        )
        if base is not UNSET:
            field_dict["base"] = base

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_vm_file_restore_entries_response_200_data_entries_item import (
            ListVmFileRestoreEntriesResponse200DataEntriesItem,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        backup_id = d.pop("backup_id")

        storage = d.pop("storage")

        path = d.pop("path")

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = ListVmFileRestoreEntriesResponse200DataEntriesItem.from_dict(
                entries_item_data
            )

            entries.append(entries_item)

        def _parse_base(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        base = _parse_base(d.pop("base", UNSET))

        list_vm_file_restore_entries_response_200_data = cls(
            service_id=service_id,
            backup_id=backup_id,
            storage=storage,
            path=path,
            entries=entries,
            base=base,
        )

        list_vm_file_restore_entries_response_200_data.additional_properties = d
        return list_vm_file_restore_entries_response_200_data

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
