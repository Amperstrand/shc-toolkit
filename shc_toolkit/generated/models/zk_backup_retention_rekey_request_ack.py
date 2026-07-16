from enum import Enum


class ZkBackupRetentionRekeyRequestAck(str, Enum):
    REKEY_WITH_RETENTION = "REKEY-WITH-RETENTION"

    def __str__(self) -> str:
        return str(self.value)
