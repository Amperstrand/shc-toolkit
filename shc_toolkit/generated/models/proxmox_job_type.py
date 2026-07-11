from enum import Enum


class ProxmoxJobType(str, Enum):
    BACKUP = "backup"
    PROVISION = "provision"
    REINSTALL = "reinstall"
    RESTORE = "restore"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
