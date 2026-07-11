from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.rekey_virtual_machine_zk_backup_body_destroy_ack import (
    RekeyVirtualMachineZkBackupBodyDestroyAck,
)

if TYPE_CHECKING:
    from ..models.zk_backup_registration import ZkBackupRegistration


T = TypeVar("T", bound="RekeyVirtualMachineZkBackupBody")


@_attrs_define
class RekeyVirtualMachineZkBackupBody:
    """
    Example:
        {'destroy_ack': 'DESTROY-MY-BACKUPS', 'zk_backup': {'config': {'v': 1, 'alg': 'argon2id13', 'ctx': 'shc-vps-
            backup-v1', 'ops': 3, 'mem': 268435456, 'salt': '0f1e2d3c4b5a69788796a5b4c3d2e1f0'}, 'recipients': [{'kind':
            'password', 'pubkey': 'b3c1e4a7d20f5986cc417b0e2d9a6f3418e7c05b9a2d1f6034785c6b9e0a1d2f', 'label': 'primary'}]}}

    Attributes:
        destroy_ack (RekeyVirtualMachineZkBackupBodyDestroyAck): Literal acknowledgement that prior-generation encrypted
            backups will be unrecoverable.
        zk_backup (ZkBackupRegistration): Zero-knowledge backup registration: client-derived X25519 pubkeys + immutable
            KDF config. Exactly one recipient must be kind=password (the primary). The server never sees the password or
            private keys. Example: {'config': {'v': 1, 'alg': 'argon2id13', 'ctx': 'shc-vps-backup-v1', 'ops': 3, 'mem':
            268435456, 'salt': '0f1e2d3c4b5a69788796a5b4c3d2e1f0'}, 'recipients': [{'kind': 'password', 'pubkey':
            'b3c1e4a7d20f5986cc417b0e2d9a6f3418e7c05b9a2d1f6034785c6b9e0a1d2f', 'label': 'primary'}]}.
    """

    destroy_ack: RekeyVirtualMachineZkBackupBodyDestroyAck
    zk_backup: ZkBackupRegistration
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destroy_ack = self.destroy_ack.value

        zk_backup = self.zk_backup.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destroy_ack": destroy_ack,
                "zk_backup": zk_backup,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.zk_backup_registration import ZkBackupRegistration

        d = dict(src_dict)
        destroy_ack = RekeyVirtualMachineZkBackupBodyDestroyAck(d.pop("destroy_ack"))

        zk_backup = ZkBackupRegistration.from_dict(d.pop("zk_backup"))

        rekey_virtual_machine_zk_backup_body = cls(
            destroy_ack=destroy_ack,
            zk_backup=zk_backup,
        )

        rekey_virtual_machine_zk_backup_body.additional_properties = d
        return rekey_virtual_machine_zk_backup_body

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
