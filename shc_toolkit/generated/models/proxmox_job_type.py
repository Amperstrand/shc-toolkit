from enum import StrEnum


class ProxmoxJobType(StrEnum):
    BACKUP = "backup"
    PROVISION = "provision"
    REINSTALL = "reinstall"
    RESTORE = "restore"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
