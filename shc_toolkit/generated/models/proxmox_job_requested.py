from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProxmoxJobRequested")


@_attrs_define
class ProxmoxJobRequested:
    """Normalized request fields captured when the job was queued.

    Attributes:
        name (None | str):  Example: nightly-demo.
        mode (None | str):  Example: suspend.
        backup_id (None | str): Opaque, per-customer backup/restore-point handle (`bk_…`). Returned in place of the real
            storage volume id so the underlying Proxmox vmid/node is never disclosed. Use this value verbatim as the
            restore/delete/protection/verify/file-restore/restore-hints handle; it is mapped back to the real volume server-
            side.
        storage (None | str): Datastore class label with any per-node suffix removed. Example: pbs.
    """

    name: None | str
    mode: None | str
    backup_id: None | str
    storage: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str
        name = self.name

        mode: None | str
        mode = self.mode

        backup_id: None | str
        backup_id = self.backup_id

        storage: None | str
        storage = self.storage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mode": mode,
                "backup_id": backup_id,
                "storage": storage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        def _parse_mode(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        mode = _parse_mode(d.pop("mode"))

        def _parse_backup_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        backup_id = _parse_backup_id(d.pop("backup_id"))

        def _parse_storage(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        storage = _parse_storage(d.pop("storage"))

        proxmox_job_requested = cls(
            name=name,
            mode=mode,
            backup_id=backup_id,
            storage=storage,
        )

        proxmox_job_requested.additional_properties = d
        return proxmox_job_requested

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
