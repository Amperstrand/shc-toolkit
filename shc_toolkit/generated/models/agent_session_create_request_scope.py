from enum import Enum


class AgentSessionCreateRequestScope(str, Enum):
    OPERATE = "operate"
    READ = "read"

    def __str__(self) -> str:
        return str(self.value)
