from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.vm_metric_series import VmMetricSeries


T = TypeVar("T", bound="GetVirtualMachineMetricsResponse200DataDiskBandwidth")


@_attrs_define
class GetVirtualMachineMetricsResponse200DataDiskBandwidth:
    """
    Attributes:
        read (VmMetricSeries): One RRD metric series. values is an array of [epoch_seconds, value] pairs. divider (when
            present) converts raw values to display units.
        write (VmMetricSeries): One RRD metric series. values is an array of [epoch_seconds, value] pairs. divider (when
            present) converts raw values to display units.
    """

    read: VmMetricSeries
    write: VmMetricSeries

    def to_dict(self) -> dict[str, Any]:
        read = self.read.to_dict()

        write = self.write.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "read": read,
                "write": write,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_metric_series import VmMetricSeries

        d = dict(src_dict)
        read = VmMetricSeries.from_dict(d.pop("read"))

        write = VmMetricSeries.from_dict(d.pop("write"))

        get_virtual_machine_metrics_response_200_data_disk_bandwidth = cls(
            read=read,
            write=write,
        )

        return get_virtual_machine_metrics_response_200_data_disk_bandwidth
