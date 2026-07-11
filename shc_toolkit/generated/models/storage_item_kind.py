from enum import Enum


class StorageItemKind(str, Enum):
    BACKUP = "backup"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
