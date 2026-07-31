from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.zk_backup_retention_rekey_request_ack import (
    ZkBackupRetentionRekeyRequestAck,
    check_zk_backup_retention_rekey_request_ack,
)

if TYPE_CHECKING:
    from ..models.zk_backup_registration import ZkBackupRegistration


T = TypeVar("T", bound="ZkBackupRetentionRekeyRequest")


@_attrs_define
class ZkBackupRetentionRekeyRequest:
    """Rotate-forward ZK backup rekey request. Future backups use the submitted recipient set; existing backups stay
    openable by their sealed recovery keys until the customer re-uploads the backups they care about.

    """

    ack: ZkBackupRetentionRekeyRequestAck
    """ Acknowledges rotate-forward self-custody: future backups use the new recipient set and existing backups stay
    openable by their sealed recovery keys until customer re-upload. """
    retain_fingerprints: list[str]
    """ Currently-active recipient fingerprints that must be carried forward into the submitted new recipient set.
    """
    zk_backup: ZkBackupRegistration
    """ Zero-knowledge backup registration: client-derived X25519 pubkeys + immutable KDF config. Exactly one
    recipient must be kind=password (the primary). The server never sees the password or private keys. """

    def to_dict(self) -> dict[str, Any]:
        ack: str = self.ack

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.zk_backup_registration import ZkBackupRegistration

        d = dict(src_dict)
        ack = check_zk_backup_retention_rekey_request_ack(d.pop("ack"))

        retain_fingerprints = cast(list[str], d.pop("retain_fingerprints"))

        zk_backup = ZkBackupRegistration.from_dict(d.pop("zk_backup"))

        zk_backup_retention_rekey_request = cls(
            ack=ack,
            retain_fingerprints=retain_fingerprints,
            zk_backup=zk_backup,
        )

        return zk_backup_retention_rekey_request
