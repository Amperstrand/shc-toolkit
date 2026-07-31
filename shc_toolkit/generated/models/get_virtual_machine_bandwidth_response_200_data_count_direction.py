from typing import Literal

GetVirtualMachineBandwidthResponse200DataCountDirection = Literal[
    "both", "inbound", "outbound"
]

GET_VIRTUAL_MACHINE_BANDWIDTH_RESPONSE_200_DATA_COUNT_DIRECTION_VALUES: set[
    GetVirtualMachineBandwidthResponse200DataCountDirection
] = {
    "both",
    "inbound",
    "outbound",
}


def check_get_virtual_machine_bandwidth_response_200_data_count_direction(
    value: str,
) -> GetVirtualMachineBandwidthResponse200DataCountDirection:
    if value in GET_VIRTUAL_MACHINE_BANDWIDTH_RESPONSE_200_DATA_COUNT_DIRECTION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_VIRTUAL_MACHINE_BANDWIDTH_RESPONSE_200_DATA_COUNT_DIRECTION_VALUES!r}"
    )
