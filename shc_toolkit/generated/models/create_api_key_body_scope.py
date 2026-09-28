from enum import StrEnum


class CreateApiKeyBodyScope(StrEnum):
    FULL = "full"
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
