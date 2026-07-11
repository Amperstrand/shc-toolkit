from enum import Enum


class CreateApiKeyBodyScope(str, Enum):
    FULL = "full"
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
