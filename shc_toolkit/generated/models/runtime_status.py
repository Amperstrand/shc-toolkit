from enum import Enum


class RuntimeStatus(str, Enum):
    PAUSED = "paused"
    RUNNING = "running"
    STOPPED = "stopped"
    SUSPENDED = "suspended"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
