from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.vm_metric_series import VmMetricSeries


T = TypeVar("T", bound="GetVirtualMachineMetricsResponse200DataNetworkBandwidth")


@_attrs_define
class GetVirtualMachineMetricsResponse200DataNetworkBandwidth:
    """
    Attributes:
        in_ (VmMetricSeries): One RRD metric series. values is an array of [epoch_seconds, value] pairs. divider (when
            present) converts raw values to display units.
        out (VmMetricSeries): One RRD metric series. values is an array of [epoch_seconds, value] pairs. divider (when
            present) converts raw values to display units.
    """

    in_: VmMetricSeries
    out: VmMetricSeries

    def to_dict(self) -> dict[str, Any]:
        in_ = self.in_.to_dict()

        out = self.out.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "in": in_,
                "out": out,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_metric_series import VmMetricSeries

        d = dict(src_dict)
        in_ = VmMetricSeries.from_dict(d.pop("in"))

        out = VmMetricSeries.from_dict(d.pop("out"))

        get_virtual_machine_metrics_response_200_data_network_bandwidth = cls(
            in_=in_,
            out=out,
        )

        return get_virtual_machine_metrics_response_200_data_network_bandwidth
