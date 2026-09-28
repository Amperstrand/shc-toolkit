from enum import StrEnum


class VmResumeResponseState(StrEnum):
    ACTIVE = "active"

    def __str__(self) -> str:
        return str(self.value)
