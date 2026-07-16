from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.zk_backup_status_envelope import ZkBackupStatusEnvelope


T = TypeVar("T", bound="RevokeVirtualMachineZkBackupRecipientResponse200")


@_attrs_define
class RevokeVirtualMachineZkBackupRecipientResponse200:
    """
    Attributes:
        data (ZkBackupStatusEnvelope):
    """

    data: ZkBackupStatusEnvelope

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.zk_backup_status_envelope import ZkBackupStatusEnvelope

        d = dict(src_dict)
        data = ZkBackupStatusEnvelope.from_dict(d.pop("data"))

        revoke_virtual_machine_zk_backup_recipient_response_200 = cls(
            data=data,
        )

        return revoke_virtual_machine_zk_backup_recipient_response_200
