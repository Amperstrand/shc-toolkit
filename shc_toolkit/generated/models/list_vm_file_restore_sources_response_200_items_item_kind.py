from enum import StrEnum


class ListVmFileRestoreSourcesResponse200ItemsItemKind(StrEnum):
    BACKUP = "backup"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
