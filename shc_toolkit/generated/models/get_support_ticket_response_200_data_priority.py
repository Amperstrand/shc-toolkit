from enum import Enum


class GetSupportTicketResponse200DataPriority(str, Enum):
    CRITICAL = "critical"
    EMERGENCY = "emergency"
    HIGH = "high"
    LOW = "low"
    MEDIUM = "medium"

    def __str__(self) -> str:
        return str(self.value)
