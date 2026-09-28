from enum import StrEnum


class VmStandbyResponseState(StrEnum):
    STANDBY = "standby"

    def __str__(self) -> str:
        return str(self.value)
