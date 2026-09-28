from enum import StrEnum


class VmBackupCreateRequestMode(StrEnum):
    SNAPSHOT = "snapshot"
    STOP = "stop"
    SUSPEND = "suspend"

    def __str__(self) -> str:
        return str(self.value)
