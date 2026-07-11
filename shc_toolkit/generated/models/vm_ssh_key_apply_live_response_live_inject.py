from enum import Enum


class VmSshKeyApplyLiveResponseLiveInject(str, Enum):
    ATTEMPTED = "attempted"

    def __str__(self) -> str:
        return str(self.value)
