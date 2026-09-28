from enum import StrEnum


class RuntimeStatus(StrEnum):
    PAUSED = "paused"
    RUNNING = "running"
    STOPPED = "stopped"
    SUSPENDED = "suspended"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
