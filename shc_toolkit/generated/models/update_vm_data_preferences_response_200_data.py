from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_vm_data_preferences_response_200_data_backup import (
        UpdateVmDataPreferencesResponse200DataBackup,
    )
    from ..models.update_vm_data_preferences_response_200_data_notify import (
        UpdateVmDataPreferencesResponse200DataNotify,
    )
    from ..models.update_vm_data_preferences_response_200_data_snapshot import (
        UpdateVmDataPreferencesResponse200DataSnapshot,
    )


T = TypeVar("T", bound="UpdateVmDataPreferencesResponse200Data")


@_attrs_define
class UpdateVmDataPreferencesResponse200Data:
    """
    Attributes:
        service_id (int):
        backup (UpdateVmDataPreferencesResponse200DataBackup):
        snapshot (UpdateVmDataPreferencesResponse200DataSnapshot):
        notify (UpdateVmDataPreferencesResponse200DataNotify):
        encryption_pubkey_set (bool): Reserved; not applied to backups (client-side backup encryption is not yet
            available).
        encryption_pubkey_fingerprint (None | str | Unset): Reserved; not applied to backups (client-side backup
            encryption is not yet available).
    """

    service_id: int
    backup: UpdateVmDataPreferencesResponse200DataBackup
    snapshot: UpdateVmDataPreferencesResponse200DataSnapshot
    notify: UpdateVmDataPreferencesResponse200DataNotify
    encryption_pubkey_set: bool
    encryption_pubkey_fingerprint: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        backup = self.backup.to_dict()

        snapshot = self.snapshot.to_dict()

        notify = self.notify.to_dict()

        encryption_pubkey_set = self.encryption_pubkey_set

        encryption_pubkey_fingerprint: None | str | Unset
        if isinstance(self.encryption_pubkey_fingerprint, Unset):
            encryption_pubkey_fingerprint = UNSET
        else:
            encryption_pubkey_fingerprint = self.encryption_pubkey_fingerprint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "backup": backup,
                "snapshot": snapshot,
                "notify": notify,
                "encryption_pubkey_set": encryption_pubkey_set,
            }
        )
        if encryption_pubkey_fingerprint is not UNSET:
            field_dict["encryption_pubkey_fingerprint"] = encryption_pubkey_fingerprint

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_vm_data_preferences_response_200_data_backup import (
            UpdateVmDataPreferencesResponse200DataBackup,
        )
        from ..models.update_vm_data_preferences_response_200_data_notify import (
            UpdateVmDataPreferencesResponse200DataNotify,
        )
        from ..models.update_vm_data_preferences_response_200_data_snapshot import (
            UpdateVmDataPreferencesResponse200DataSnapshot,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        backup = UpdateVmDataPreferencesResponse200DataBackup.from_dict(d.pop("backup"))

        snapshot = UpdateVmDataPreferencesResponse200DataSnapshot.from_dict(
            d.pop("snapshot")
        )

        notify = UpdateVmDataPreferencesResponse200DataNotify.from_dict(d.pop("notify"))

        encryption_pubkey_set = d.pop("encryption_pubkey_set")

        def _parse_encryption_pubkey_fingerprint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        encryption_pubkey_fingerprint = _parse_encryption_pubkey_fingerprint(
            d.pop("encryption_pubkey_fingerprint", UNSET)
        )

        update_vm_data_preferences_response_200_data = cls(
            service_id=service_id,
            backup=backup,
            snapshot=snapshot,
            notify=notify,
            encryption_pubkey_set=encryption_pubkey_set,
            encryption_pubkey_fingerprint=encryption_pubkey_fingerprint,
        )

        update_vm_data_preferences_response_200_data.additional_properties = d
        return update_vm_data_preferences_response_200_data

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
