from enum import Enum


class VmStandbyResponseIpDisposition(str, Enum):
    KEPT = "kept"
    RELEASED = "released"

    def __str__(self) -> str:
        return str(self.value)
