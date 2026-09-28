from enum import StrEnum


class AgentSessionCreateRequestScope(StrEnum):
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
