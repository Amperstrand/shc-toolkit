from enum import StrEnum


class CloudInitApplyResultVolumeLabel(StrEnum):
    CIDATA = "CIDATA"

    def __str__(self) -> str:
        return str(self.value)
