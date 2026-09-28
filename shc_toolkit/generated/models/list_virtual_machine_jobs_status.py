from enum import StrEnum


class ListVirtualMachineJobsStatus(StrEnum):
    CANCELED = "canceled"
    COMPLETED = "completed"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
