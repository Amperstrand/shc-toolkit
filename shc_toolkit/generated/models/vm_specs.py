from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmSpecs")


@_attrs_define
class VmSpecs:
    """Package-derived resource profile for a VM service or plan.

    Example:
        {'cpu': 2, 'memory_mb': 4096, 'disk_gb': 80, 'bandwidth_gb': 4000, 'ipv4': 1, 'ipv6': 1}

    Attributes:
        cpu (int): vCPU count from package metadata. Example: 2.
        memory_mb (int): Provisioned memory in megabytes. Example: 4096.
        disk_gb (int): Primary disk allocation in gigabytes. Example: 80.
        bandwidth_gb (int): Included transfer allowance in gigabytes. Example: 4000.
        ipv4 (int): Count of IPv4 addresses included in the package metadata. Example: 1.
        ipv6 (int): Count of IPv6 addresses included in the package metadata. Example: 1.
    """

    cpu: int
    memory_mb: int
    disk_gb: int
    bandwidth_gb: int
    ipv4: int
    ipv6: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu = self.cpu

        memory_mb = self.memory_mb

        disk_gb = self.disk_gb

        bandwidth_gb = self.bandwidth_gb

        ipv4 = self.ipv4

        ipv6 = self.ipv6

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpu": cpu,
                "memory_mb": memory_mb,
                "disk_gb": disk_gb,
                "bandwidth_gb": bandwidth_gb,
                "ipv4": ipv4,
                "ipv6": ipv6,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cpu = d.pop("cpu")

        memory_mb = d.pop("memory_mb")

        disk_gb = d.pop("disk_gb")

        bandwidth_gb = d.pop("bandwidth_gb")

        ipv4 = d.pop("ipv4")

        ipv6 = d.pop("ipv6")

        vm_specs = cls(
            cpu=cpu,
            memory_mb=memory_mb,
            disk_gb=disk_gb,
            bandwidth_gb=bandwidth_gb,
            ipv4=ipv4,
            ipv6=ipv6,
        )

        vm_specs.additional_properties = d
        return vm_specs

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
