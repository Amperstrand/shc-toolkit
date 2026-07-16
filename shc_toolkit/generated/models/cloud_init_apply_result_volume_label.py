from enum import Enum


class CloudInitApplyResultVolumeLabel(str, Enum):
    CIDATA = "CIDATA"

    def __str__(self) -> str:
        return str(self.value)
