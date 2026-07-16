from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_data_preferences_update_request_backup import (
        VmDataPreferencesUpdateRequestBackup,
    )
    from ..models.vm_data_preferences_update_request_notify import (
        VmDataPreferencesUpdateRequestNotify,
    )
    from ..models.vm_data_preferences_update_request_snapshot import (
        VmDataPreferencesUpdateRequestSnapshot,
    )
    from ..models.zk_backup_registration import ZkBackupRegistration


T = TypeVar("T", bound="VmDataPreferencesUpdateRequest")


@_attrs_define
class VmDataPreferencesUpdateRequest:
    """Update backup/snapshot schedule, retention, notification, and encryption-pubkey preferences. PATCH semantics: only
    the sections/keys present are changed. At least one recognized field is expected. If zk_backup is supplied for first
    registration, X-User-Api-Confirm is required before the initial recipient set is written.

        Example:
            {'backup': {'retention': 'keep-daily=7', 'auto_days': ['mon', 'thu'], 'auto_time': '03:00'}, 'notify':
                {'failed': True, 'success': False}}

        Attributes:
            backup (VmDataPreferencesUpdateRequestBackup | Unset): Backup or snapshot scheduling preferences. Only the keys
                present are updated (PATCH semantics).
            snapshot (VmDataPreferencesUpdateRequestSnapshot | Unset): Backup or snapshot scheduling preferences. Only the
                keys present are updated (PATCH semantics).
            notify (VmDataPreferencesUpdateRequestNotify | Unset): Notification toggles. Each accepts a JSON boolean or the
                strings on/off/true/false/1/0.
            encryption_pubkey (None | str | Unset): Reserved — client-side backup encryption is not yet available; a non-
                empty value returns 501.
            zk_backup (ZkBackupRegistration | Unset): Zero-knowledge backup registration: client-derived X25519 pubkeys +
                immutable KDF config. Exactly one recipient must be kind=password (the primary). The server never sees the
                password or private keys. Example: {'config': {'v': 1, 'alg': 'argon2id13', 'ctx': 'shc-vps-backup-v1', 'ops':
                3, 'mem': 268435456, 'salt': '0f1e2d3c4b5a69788796a5b4c3d2e1f0'}, 'recipients': [{'kind': 'password', 'pubkey':
                'b3c1e4a7d20f5986cc417b0e2d9a6f3418e7c05b9a2d1f6034785c6b9e0a1d2f', 'label': 'primary'}]}.
    """

    backup: VmDataPreferencesUpdateRequestBackup | Unset = UNSET
    snapshot: VmDataPreferencesUpdateRequestSnapshot | Unset = UNSET
    notify: VmDataPreferencesUpdateRequestNotify | Unset = UNSET
    encryption_pubkey: None | str | Unset = UNSET
    zk_backup: ZkBackupRegistration | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        backup: dict[str, Any] | Unset = UNSET
        if not isinstance(self.backup, Unset):
            backup = self.backup.to_dict()

        snapshot: dict[str, Any] | Unset = UNSET
        if not isinstance(self.snapshot, Unset):
            snapshot = self.snapshot.to_dict()

        notify: dict[str, Any] | Unset = UNSET
        if not isinstance(self.notify, Unset):
            notify = self.notify.to_dict()

        encryption_pubkey: None | str | Unset
        if isinstance(self.encryption_pubkey, Unset):
            encryption_pubkey = UNSET
        else:
            encryption_pubkey = self.encryption_pubkey

        zk_backup: dict[str, Any] | Unset = UNSET
        if not isinstance(self.zk_backup, Unset):
            zk_backup = self.zk_backup.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if backup is not UNSET:
            field_dict["backup"] = backup
        if snapshot is not UNSET:
            field_dict["snapshot"] = snapshot
        if notify is not UNSET:
            field_dict["notify"] = notify
        if encryption_pubkey is not UNSET:
            field_dict["encryption_pubkey"] = encryption_pubkey
        if zk_backup is not UNSET:
            field_dict["zk_backup"] = zk_backup

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_data_preferences_update_request_backup import (
            VmDataPreferencesUpdateRequestBackup,
        )
        from ..models.vm_data_preferences_update_request_notify import (
            VmDataPreferencesUpdateRequestNotify,
        )
        from ..models.vm_data_preferences_update_request_snapshot import (
            VmDataPreferencesUpdateRequestSnapshot,
        )
        from ..models.zk_backup_registration import ZkBackupRegistration

        d = dict(src_dict)
        _backup = d.pop("backup", UNSET)
        backup: VmDataPreferencesUpdateRequestBackup | Unset
        if isinstance(_backup, Unset):
            backup = UNSET
        else:
            backup = VmDataPreferencesUpdateRequestBackup.from_dict(_backup)

        _snapshot = d.pop("snapshot", UNSET)
        snapshot: VmDataPreferencesUpdateRequestSnapshot | Unset
        if isinstance(_snapshot, Unset):
            snapshot = UNSET
        else:
            snapshot = VmDataPreferencesUpdateRequestSnapshot.from_dict(_snapshot)

        _notify = d.pop("notify", UNSET)
        notify: VmDataPreferencesUpdateRequestNotify | Unset
        if isinstance(_notify, Unset):
            notify = UNSET
        else:
            notify = VmDataPreferencesUpdateRequestNotify.from_dict(_notify)

        def _parse_encryption_pubkey(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        encryption_pubkey = _parse_encryption_pubkey(d.pop("encryption_pubkey", UNSET))

        _zk_backup = d.pop("zk_backup", UNSET)
        zk_backup: ZkBackupRegistration | Unset
        if isinstance(_zk_backup, Unset):
            zk_backup = UNSET
        else:
            zk_backup = ZkBackupRegistration.from_dict(_zk_backup)

        vm_data_preferences_update_request = cls(
            backup=backup,
            snapshot=snapshot,
            notify=notify,
            encryption_pubkey=encryption_pubkey,
            zk_backup=zk_backup,
        )

        return vm_data_preferences_update_request
