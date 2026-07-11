from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_vm_file_restore_sources_response_200_items_item_kind import (
    ListVmFileRestoreSourcesResponse200ItemsItemKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListVmFileRestoreSourcesResponse200ItemsItem")


@_attrs_define
class ListVmFileRestoreSourcesResponse200ItemsItem:
    """
    Attributes:
        kind (ListVmFileRestoreSourcesResponse200ItemsItemKind):
        backup_id (str): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the real
            storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side. Example: bk_6ERwSd_PLY66FW72VFM.
        label (str):
        encrypted (bool):
        name (str | Unset):
        storage (None | str | Unset):
        notes (None | str | Unset):
        size_bytes (int | None | Unset):
        protected (bool | Unset):
        created_at (datetime.datetime | None | Unset):
        created_epoch (int | None | Unset):
    """

    kind: ListVmFileRestoreSourcesResponse200ItemsItemKind
    backup_id: str
    label: str
    encrypted: bool
    name: str | Unset = UNSET
    storage: None | str | Unset = UNSET
    notes: None | str | Unset = UNSET
    size_bytes: int | None | Unset = UNSET
    protected: bool | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    created_epoch: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        backup_id = self.backup_id

        label = self.label

        encrypted = self.encrypted

        name = self.name

        storage: None | str | Unset
        if isinstance(self.storage, Unset):
            storage = UNSET
        else:
            storage = self.storage

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        size_bytes: int | None | Unset
        if isinstance(self.size_bytes, Unset):
            size_bytes = UNSET
        else:
            size_bytes = self.size_bytes

        protected = self.protected

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        created_epoch: int | None | Unset
        if isinstance(self.created_epoch, Unset):
            created_epoch = UNSET
        else:
            created_epoch = self.created_epoch

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "backup_id": backup_id,
                "label": label,
                "encrypted": encrypted,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if storage is not UNSET:
            field_dict["storage"] = storage
        if notes is not UNSET:
            field_dict["notes"] = notes
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if protected is not UNSET:
            field_dict["protected"] = protected
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if created_epoch is not UNSET:
            field_dict["created_epoch"] = created_epoch

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = ListVmFileRestoreSourcesResponse200ItemsItemKind(d.pop("kind"))

        backup_id = d.pop("backup_id")

        label = d.pop("label")

        encrypted = d.pop("encrypted")

        name = d.pop("name", UNSET)

        def _parse_storage(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        storage = _parse_storage(d.pop("storage", UNSET))

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        def _parse_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes", UNSET))

        protected = d.pop("protected", UNSET)

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_created_epoch(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        created_epoch = _parse_created_epoch(d.pop("created_epoch", UNSET))

        list_vm_file_restore_sources_response_200_items_item = cls(
            kind=kind,
            backup_id=backup_id,
            label=label,
            encrypted=encrypted,
            name=name,
            storage=storage,
            notes=notes,
            size_bytes=size_bytes,
            protected=protected,
            created_at=created_at,
            created_epoch=created_epoch,
        )

        list_vm_file_restore_sources_response_200_items_item.additional_properties = d
        return list_vm_file_restore_sources_response_200_items_item

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
