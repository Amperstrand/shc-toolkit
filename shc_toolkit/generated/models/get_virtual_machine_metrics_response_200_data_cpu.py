from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.vm_metric_series import VmMetricSeries


T = TypeVar("T", bound="GetVirtualMachineMetricsResponse200DataCpu")


@_attrs_define
class GetVirtualMachineMetricsResponse200DataCpu:
    """
    Attributes:
        cpu (VmMetricSeries): One RRD metric series. values is an array of [epoch_seconds, value] pairs. divider (when
            present) converts raw values to display units.
    """

    cpu: VmMetricSeries

    def to_dict(self) -> dict[str, Any]:
        cpu = self.cpu.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "cpu": cpu,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_metric_series import VmMetricSeries

        d = dict(src_dict)
        cpu = VmMetricSeries.from_dict(d.pop("cpu"))

        get_virtual_machine_metrics_response_200_data_cpu = cls(
            cpu=cpu,
        )

        return get_virtual_machine_metrics_response_200_data_cpu
