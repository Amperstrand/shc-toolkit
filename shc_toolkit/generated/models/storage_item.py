from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.storage_item_kind import StorageItemKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="StorageItem")


@_attrs_define
class StorageItem:
    """Backup or snapshot volume currently visible for the owned VM service.

    Attributes:
        kind (StorageItemKind):  Example: backup.
        backup_id (str): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the real
            storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side. Example: bk_6ERwSd_PLY66FW72VFM.
        name (str):  Example: nightly-demo.
        storage (None | str): Datastore class label with any per-node suffix removed (never reveals the host node).
            Example: pbs-backups.
        notes (None | str):  Example: nightly-demo.
        size_bytes (int | None):  Example: 2147483648.
        protected (bool):
        encrypted (bool):  Example: True.
        created_at (datetime.datetime | None):  Example: 2026-04-17T01:23:45+00:00.
        created_epoch (int | None): Unix timestamp (seconds since 1970-01-01 UTC). Surfaced alongside `created_at` for
            clients that prefer a numeric value. Example: 1745895825.
        id (str | Unset): v2.4.0 alias (additive): identical to backup_id (the opaque handle).
        snapshot_id (str | Unset): v2.4.0 alias (additive): present on kind=snapshot items only; identical to backup_id.
            Write bodies accept backup_id | snapshot_id | id | volid.
    """

    kind: StorageItemKind
    backup_id: str
    name: str
    storage: None | str
    notes: None | str
    size_bytes: int | None
    protected: bool
    encrypted: bool
    created_at: datetime.datetime | None
    created_epoch: int | None
    id: str | Unset = UNSET
    snapshot_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        backup_id = self.backup_id

        name = self.name

        storage: None | str
        storage = self.storage

        notes: None | str
        notes = self.notes

        size_bytes: int | None
        size_bytes = self.size_bytes

        protected = self.protected

        encrypted = self.encrypted

        created_at: None | str
        if isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        created_epoch: int | None
        created_epoch = self.created_epoch

        id = self.id

        snapshot_id = self.snapshot_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "backup_id": backup_id,
                "name": name,
                "storage": storage,
                "notes": notes,
                "size_bytes": size_bytes,
                "protected": protected,
                "encrypted": encrypted,
                "created_at": created_at,
                "created_epoch": created_epoch,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if snapshot_id is not UNSET:
            field_dict["snapshot_id"] = snapshot_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = StorageItemKind(d.pop("kind"))

        backup_id = d.pop("backup_id")

        name = d.pop("name")

        def _parse_storage(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        storage = _parse_storage(d.pop("storage"))

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        def _parse_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes"))

        protected = d.pop("protected")

        encrypted = d.pop("encrypted")

        def _parse_created_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        created_at = _parse_created_at(d.pop("created_at"))

        def _parse_created_epoch(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        created_epoch = _parse_created_epoch(d.pop("created_epoch"))

        id = d.pop("id", UNSET)

        snapshot_id = d.pop("snapshot_id", UNSET)

        storage_item = cls(
            kind=kind,
            backup_id=backup_id,
            name=name,
            storage=storage,
            notes=notes,
            size_bytes=size_bytes,
            protected=protected,
            encrypted=encrypted,
            created_at=created_at,
            created_epoch=created_epoch,
            id=id,
            snapshot_id=snapshot_id,
        )

        storage_item.additional_properties = d
        return storage_item

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
