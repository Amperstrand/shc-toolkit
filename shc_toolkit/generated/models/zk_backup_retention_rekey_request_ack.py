from enum import StrEnum


class ZkBackupRetentionRekeyRequestAck(StrEnum):
    REKEY_WITH_RETENTION = "REKEY-WITH-RETENTION"

    def __str__(self) -> str:
        return str(self.value)
