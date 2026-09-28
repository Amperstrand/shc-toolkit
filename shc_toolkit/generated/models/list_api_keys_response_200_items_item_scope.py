from enum import StrEnum


class ListApiKeysResponse200ItemsItemScope(StrEnum):
    FULL = "full"
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
