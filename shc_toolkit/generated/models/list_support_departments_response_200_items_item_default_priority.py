from enum import StrEnum


class ListSupportDepartmentsResponse200ItemsItemDefaultPriority(StrEnum):
    CRITICAL = "critical"
    EMERGENCY = "emergency"
    HIGH = "high"
    LOW = "low"
    MEDIUM = "medium"

    def __str__(self) -> str:
        return str(self.value)
