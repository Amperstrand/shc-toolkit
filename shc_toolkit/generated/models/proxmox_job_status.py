from enum import Enum


class ProxmoxJobStatus(str, Enum):
    CANCELED = "canceled"
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
