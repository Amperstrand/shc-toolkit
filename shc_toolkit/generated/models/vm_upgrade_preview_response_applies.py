from enum import StrEnum


class VmUpgradePreviewResponseApplies(StrEnum):
    QUEUED = "queued"

    def __str__(self) -> str:
        return str(self.value)
