from typing import Literal

GetVirtualMachineMetricsResponse200DataTimeframe = Literal[
    "day", "hour", "month", "week", "year"
]

GET_VIRTUAL_MACHINE_METRICS_RESPONSE_200_DATA_TIMEFRAME_VALUES: set[
    GetVirtualMachineMetricsResponse200DataTimeframe
] = {
    "day",
    "hour",
    "month",
    "week",
    "year",
}


def check_get_virtual_machine_metrics_response_200_data_timeframe(
    value: str,
) -> GetVirtualMachineMetricsResponse200DataTimeframe:
    if value in GET_VIRTUAL_MACHINE_METRICS_RESPONSE_200_DATA_TIMEFRAME_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_VIRTUAL_MACHINE_METRICS_RESPONSE_200_DATA_TIMEFRAME_VALUES!r}"
    )
