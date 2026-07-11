from enum import Enum


class GetVirtualMachineMetricsTimeframe(str, Enum):
    DAY = "day"
    HOUR = "hour"
    MONTH = "month"
    WEEK = "week"
    YEAR = "year"

    def __str__(self) -> str:
        return str(self.value)
