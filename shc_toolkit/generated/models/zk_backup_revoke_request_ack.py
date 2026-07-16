from enum import Enum


class ZkBackupRevokeRequestAck(str, Enum):
    REVOKE_FUTURE_SEALS = "REVOKE-FUTURE-SEALS"

    def __str__(self) -> str:
        return str(self.value)
