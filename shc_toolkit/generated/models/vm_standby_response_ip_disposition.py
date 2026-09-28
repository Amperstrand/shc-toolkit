from enum import StrEnum


class VmStandbyResponseIpDisposition(StrEnum):
    KEPT = "kept"
    RELEASED = "released"

    def __str__(self) -> str:
        return str(self.value)
