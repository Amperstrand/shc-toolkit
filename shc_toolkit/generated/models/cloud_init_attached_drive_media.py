from enum import Enum


class CloudInitAttachedDriveMedia(str, Enum):
    CDROM = "cdrom"

    def __str__(self) -> str:
        return str(self.value)
