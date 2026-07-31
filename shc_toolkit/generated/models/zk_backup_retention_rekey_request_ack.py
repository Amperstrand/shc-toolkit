from typing import Literal

ZkBackupRetentionRekeyRequestAck = Literal["REKEY-WITH-RETENTION"]

ZK_BACKUP_RETENTION_REKEY_REQUEST_ACK_VALUES: set[ZkBackupRetentionRekeyRequestAck] = {
    "REKEY-WITH-RETENTION",
}


def check_zk_backup_retention_rekey_request_ack(
    value: str,
) -> ZkBackupRetentionRekeyRequestAck:
    if value in ZK_BACKUP_RETENTION_REKEY_REQUEST_ACK_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ZK_BACKUP_RETENTION_REKEY_REQUEST_ACK_VALUES!r}"
    )
