from enum import Enum


class ListVmFileRestoreSourcesResponse200ItemsItemKind(str, Enum):
    BACKUP = "backup"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
