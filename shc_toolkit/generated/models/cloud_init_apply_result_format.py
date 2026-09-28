from enum import StrEnum


class CloudInitApplyResultFormat(StrEnum):
    VFAT = "vfat"

    def __str__(self) -> str:
        return str(self.value)
