from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.zk_backup_revoke_request_ack import ZkBackupRevokeRequestAck

T = TypeVar("T", bound="ZkBackupRevokeRequest")


@_attrs_define
class ZkBackupRevokeRequest:
    """
    Attributes:
        fingerprint (str):
        ack (ZkBackupRevokeRequestAck): Acknowledges rotate-forward self-custody: revocation stops future seals to this
            recipient, while already sealed backups stay openable by their sealed recovery keys until customer re-upload.
    """

    fingerprint: str
    ack: ZkBackupRevokeRequestAck

    def to_dict(self) -> dict[str, Any]:
        fingerprint = self.fingerprint

        ack = self.ack.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "fingerprint": fingerprint,
                "ack": ack,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fingerprint = d.pop("fingerprint")

        ack = ZkBackupRevokeRequestAck(d.pop("ack"))

        zk_backup_revoke_request = cls(
            fingerprint=fingerprint,
            ack=ack,
        )

        return zk_backup_revoke_request
