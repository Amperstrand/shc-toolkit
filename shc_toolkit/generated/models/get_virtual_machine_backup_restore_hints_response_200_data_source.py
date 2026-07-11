from enum import Enum


class GetVirtualMachineBackupRestoreHintsResponse200DataSource(str, Enum):
    BACKUP = "backup"

    def __str__(self) -> str:
        return str(self.value)
