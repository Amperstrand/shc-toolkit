from enum import StrEnum


class StorageItemKind(StrEnum):
    BACKUP = "backup"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
