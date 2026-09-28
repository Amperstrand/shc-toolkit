from enum import StrEnum


class VmUpgradeResponseChange(StrEnum):
    QUEUED = "queued"

    def __str__(self) -> str:
        return str(self.value)
