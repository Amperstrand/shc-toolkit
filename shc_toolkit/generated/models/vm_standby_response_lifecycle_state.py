from enum import StrEnum


class VmStandbyResponseLifecycleState(StrEnum):
    STANDBY = "standby"

    def __str__(self) -> str:
        return str(self.value)
