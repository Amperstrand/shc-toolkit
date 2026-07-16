from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.zk_backup_recipient_set_status import ZkBackupRecipientSetStatus


T = TypeVar("T", bound="ZkBackupStatusEnvelope")


@_attrs_define
class ZkBackupStatusEnvelope:
    """
    Attributes:
        service_id (int):
        zk_backup (ZkBackupRecipientSetStatus): Verified owner-visible ZK backup recipient set, including revoked
            recipients. SHC ZK backup is genuine self-custody, the same model as Bitcoin: your keys, your data. Backups
            already sealed to a recovery key stay openable by that key until you rotate forward and re-upload the backups
            you care about; that is the sovereignty property. If a recovery key is exposed, register a fresh recipient set
            and re-upload replacement backups, like sweeping a Bitcoin key to a fresh address. SHC cannot re-seal, claw
            back, or reach into existing backup data; that inability is the guarantee.
    """

    service_id: int
    zk_backup: ZkBackupRecipientSetStatus

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        zk_backup = self.zk_backup.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "zk_backup": zk_backup,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.zk_backup_recipient_set_status import ZkBackupRecipientSetStatus

        d = dict(src_dict)
        service_id = d.pop("service_id")

        zk_backup = ZkBackupRecipientSetStatus.from_dict(d.pop("zk_backup"))

        zk_backup_status_envelope = cls(
            service_id=service_id,
            zk_backup=zk_backup,
        )

        return zk_backup_status_envelope
