from typing import Literal

GetVirtualMachineMetricsTimeframe = Literal["day", "hour", "month", "week", "year"]

GET_VIRTUAL_MACHINE_METRICS_TIMEFRAME_VALUES: set[GetVirtualMachineMetricsTimeframe] = {
    "day",
    "hour",
    "month",
    "week",
    "year",
}


def check_get_virtual_machine_metrics_timeframe(
    value: str,
) -> GetVirtualMachineMetricsTimeframe:
    if value in GET_VIRTUAL_MACHINE_METRICS_TIMEFRAME_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_VIRTUAL_MACHINE_METRICS_TIMEFRAME_VALUES!r}"
    )
