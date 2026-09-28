from enum import StrEnum


class VmResumeResponseLifecycleState(StrEnum):
    ACTIVE = "active"

    def __str__(self) -> str:
        return str(self.value)
