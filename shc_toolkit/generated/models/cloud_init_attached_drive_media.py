from enum import StrEnum


class CloudInitAttachedDriveMedia(StrEnum):
    CDROM = "cdrom"

    def __str__(self) -> str:
        return str(self.value)
