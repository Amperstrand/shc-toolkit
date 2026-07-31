from typing import Literal

ZkBackupRevokeRequestAck = Literal["REVOKE-FUTURE-SEALS"]

ZK_BACKUP_REVOKE_REQUEST_ACK_VALUES: set[ZkBackupRevokeRequestAck] = {
    "REVOKE-FUTURE-SEALS",
}


def check_zk_backup_revoke_request_ack(value: str) -> ZkBackupRevokeRequestAck:
    if value in ZK_BACKUP_REVOKE_REQUEST_ACK_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ZK_BACKUP_REVOKE_REQUEST_ACK_VALUES!r}"
    )
