from enum import StrEnum


class VmSshKeyApplyLiveResponseLiveInject(StrEnum):
    ATTEMPTED = "attempted"

    def __str__(self) -> str:
        return str(self.value)
