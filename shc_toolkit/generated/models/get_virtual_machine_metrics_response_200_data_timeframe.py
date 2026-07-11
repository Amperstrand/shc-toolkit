from enum import Enum


class GetVirtualMachineMetricsResponse200DataTimeframe(str, Enum):
    DAY = "day"
    HOUR = "hour"
    MONTH = "month"
    WEEK = "week"
    YEAR = "year"

    def __str__(self) -> str:
        return str(self.value)
