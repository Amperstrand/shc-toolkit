from enum import StrEnum


class ClaimAgentKeyResponse200DataScope(StrEnum):
    FULL = "full"
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
