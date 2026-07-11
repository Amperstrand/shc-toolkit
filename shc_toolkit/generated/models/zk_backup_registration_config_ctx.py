from enum import Enum


class ZkBackupRegistrationConfigCtx(str, Enum):
    SHC_VPS_BACKUP_V1 = "shc-vps-backup-v1"

    def __str__(self) -> str:
        return str(self.value)
