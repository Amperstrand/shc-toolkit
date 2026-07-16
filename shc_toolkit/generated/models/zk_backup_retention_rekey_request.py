from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.zk_backup_retention_rekey_request_ack import (
    ZkBackupRetentionRekeyRequestAck,
)

if TYPE_CHECKING:
    from ..models.zk_backup_registration import ZkBackupRegistration


T = TypeVar("T", bound="ZkBackupRetentionRekeyRequest")


@_attrs_define
class ZkBackupRetentionRekeyRequest:
    """Rotate-forward ZK backup rekey request. Future backups use the submitted recipient set; existing backups stay
    openable by their sealed recovery keys until the customer re-uploads the backups they care about.

        Attributes:
            ack (ZkBackupRetentionRekeyRequestAck): Acknowledges rotate-forward self-custody: future backups use the new
                recipient set and existing backups stay openable by their sealed recovery keys until customer re-upload.
            retain_fingerprints (list[str]): Currently-active recipient fingerprints that must be carried forward into the
                submitted new recipient set.
            zk_backup (ZkBackupRegistration): Zero-knowledge backup registration: client-derived X25519 pubkeys + immutable
                KDF config. Exactly one recipient must be kind=password (the primary). The server never sees the password or
                private keys. Example: {'config': {'v': 1, 'alg': 'argon2id13', 'ctx': 'shc-vps-backup-v1', 'ops': 3, 'mem':
                268435456, 'salt': '0f1e2d3c4b5a69788796a5b4c3d2e1f0'}, 'recipients': [{'kind': 'password', 'pubkey':
                'b3c1e4a7d20f5986cc417b0e2d9a6f3418e7c05b9a2d1f6034785c6b9e0a1d2f', 'label': 'primary'}]}.
    """

    ack: ZkBackupRetentionRekeyRequestAck
    retain_fingerprints: list[str]
    zk_backup: ZkBackupRegistration

    def to_dict(self) -> dict[str, Any]:
        ack = self.ack.value

        retain_fingerprints = self.retain_fingerprints

        zk_backup = self.zk_backup.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "ack": ack,
                "retain_fingerprints": retain_fingerprints,
                "zk_backup": zk_backup,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.zk_backup_registration import ZkBackupRegistration

        d = dict(src_dict)
        ack = ZkBackupRetentionRekeyRequestAck(d.pop("ack"))

        retain_fingerprints = cast(list[str], d.pop("retain_fingerprints"))

        zk_backup = ZkBackupRegistration.from_dict(d.pop("zk_backup"))

        zk_backup_retention_rekey_request = cls(
            ack=ack,
            retain_fingerprints=retain_fingerprints,
            zk_backup=zk_backup,
        )

        return zk_backup_retention_rekey_request
