from enum import StrEnum


class AgentSessionScope(StrEnum):
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
