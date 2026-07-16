from enum import Enum


class VmResumeResponseLifecycleState(str, Enum):
    ACTIVE = "active"

    def __str__(self) -> str:
        return str(self.value)
