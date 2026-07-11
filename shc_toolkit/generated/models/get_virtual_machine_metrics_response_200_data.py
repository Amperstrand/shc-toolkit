from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.get_virtual_machine_metrics_response_200_data_timeframe import (
    GetVirtualMachineMetricsResponse200DataTimeframe,
)

if TYPE_CHECKING:
    from ..models.get_virtual_machine_metrics_response_200_data_cpu import (
        GetVirtualMachineMetricsResponse200DataCpu,
    )
    from ..models.get_virtual_machine_metrics_response_200_data_disk_bandwidth import (
        GetVirtualMachineMetricsResponse200DataDiskBandwidth,
    )
    from ..models.get_virtual_machine_metrics_response_200_data_network_bandwidth import (
        GetVirtualMachineMetricsResponse200DataNetworkBandwidth,
    )
    from ..models.get_virtual_machine_metrics_response_200_data_ram import (
        GetVirtualMachineMetricsResponse200DataRam,
    )


T = TypeVar("T", bound="GetVirtualMachineMetricsResponse200Data")


@_attrs_define
class GetVirtualMachineMetricsResponse200Data:
    """
    Attributes:
        timeframe (GetVirtualMachineMetricsResponse200DataTimeframe):  Example: hour.
        cpu (GetVirtualMachineMetricsResponse200DataCpu):
        ram (GetVirtualMachineMetricsResponse200DataRam):
        disk_bandwidth (GetVirtualMachineMetricsResponse200DataDiskBandwidth):
        network_bandwidth (GetVirtualMachineMetricsResponse200DataNetworkBandwidth):
    """

    timeframe: GetVirtualMachineMetricsResponse200DataTimeframe
    cpu: GetVirtualMachineMetricsResponse200DataCpu
    ram: GetVirtualMachineMetricsResponse200DataRam
    disk_bandwidth: GetVirtualMachineMetricsResponse200DataDiskBandwidth
    network_bandwidth: GetVirtualMachineMetricsResponse200DataNetworkBandwidth

    def to_dict(self) -> dict[str, Any]:
        timeframe = self.timeframe.value

        cpu = self.cpu.to_dict()

        ram = self.ram.to_dict()

        disk_bandwidth = self.disk_bandwidth.to_dict()

        network_bandwidth = self.network_bandwidth.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "timeframe": timeframe,
                "cpu": cpu,
                "ram": ram,
                "disk_bandwidth": disk_bandwidth,
                "network_bandwidth": network_bandwidth,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_virtual_machine_metrics_response_200_data_cpu import (
            GetVirtualMachineMetricsResponse200DataCpu,
        )
        from ..models.get_virtual_machine_metrics_response_200_data_disk_bandwidth import (
            GetVirtualMachineMetricsResponse200DataDiskBandwidth,
        )
        from ..models.get_virtual_machine_metrics_response_200_data_network_bandwidth import (
            GetVirtualMachineMetricsResponse200DataNetworkBandwidth,
        )
        from ..models.get_virtual_machine_metrics_response_200_data_ram import (
            GetVirtualMachineMetricsResponse200DataRam,
        )

        d = dict(src_dict)
        timeframe = GetVirtualMachineMetricsResponse200DataTimeframe(d.pop("timeframe"))

        cpu = GetVirtualMachineMetricsResponse200DataCpu.from_dict(d.pop("cpu"))

        ram = GetVirtualMachineMetricsResponse200DataRam.from_dict(d.pop("ram"))

        disk_bandwidth = GetVirtualMachineMetricsResponse200DataDiskBandwidth.from_dict(
            d.pop("disk_bandwidth")
        )

        network_bandwidth = (
            GetVirtualMachineMetricsResponse200DataNetworkBandwidth.from_dict(
                d.pop("network_bandwidth")
            )
        )

        get_virtual_machine_metrics_response_200_data = cls(
            timeframe=timeframe,
            cpu=cpu,
            ram=ram,
            disk_bandwidth=disk_bandwidth,
            network_bandwidth=network_bandwidth,
        )

        return get_virtual_machine_metrics_response_200_data
