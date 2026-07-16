from enum import Enum


class CloudInitApplyResultFormat(str, Enum):
    VFAT = "vfat"

    def __str__(self) -> str:
        return str(self.value)
