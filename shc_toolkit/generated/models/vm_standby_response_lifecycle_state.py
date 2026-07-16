from enum import Enum


class VmStandbyResponseLifecycleState(str, Enum):
    STANDBY = "standby"

    def __str__(self) -> str:
        return str(self.value)
