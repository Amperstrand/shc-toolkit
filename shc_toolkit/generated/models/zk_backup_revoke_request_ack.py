from enum import StrEnum


class ZkBackupRevokeRequestAck(StrEnum):
    REVOKE_FUTURE_SEALS = "REVOKE-FUTURE-SEALS"

    def __str__(self) -> str:
        return str(self.value)
