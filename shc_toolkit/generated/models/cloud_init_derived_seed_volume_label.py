from enum import StrEnum


class CloudInitDerivedSeedVolumeLabel(StrEnum):
    CIDATA = "CIDATA"

    def __str__(self) -> str:
        return str(self.value)
