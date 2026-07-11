from enum import Enum


class VmBackupCreateRequestMode(str, Enum):
    SNAPSHOT = "snapshot"
    STOP = "stop"
    SUSPEND = "suspend"

    def __str__(self) -> str:
        return str(self.value)
