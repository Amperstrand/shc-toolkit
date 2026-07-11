from enum import Enum


class ClaimAgentKeyResponse200DataScope(str, Enum):
    FULL = "full"
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
