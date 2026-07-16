from enum import Enum


class AgentSessionCreatedScope(str, Enum):
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
