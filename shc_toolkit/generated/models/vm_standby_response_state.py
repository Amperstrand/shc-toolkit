from enum import Enum


class VmStandbyResponseState(str, Enum):
    STANDBY = "standby"

    def __str__(self) -> str:
        return str(self.value)
