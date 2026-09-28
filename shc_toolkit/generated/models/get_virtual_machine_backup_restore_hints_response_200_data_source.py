from enum import StrEnum


class GetVirtualMachineBackupRestoreHintsResponse200DataSource(StrEnum):
    BACKUP = "backup"

    def __str__(self) -> str:
        return str(self.value)
