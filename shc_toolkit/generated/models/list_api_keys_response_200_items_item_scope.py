from enum import Enum


class ListApiKeysResponse200ItemsItemScope(str, Enum):
    FULL = "full"
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
