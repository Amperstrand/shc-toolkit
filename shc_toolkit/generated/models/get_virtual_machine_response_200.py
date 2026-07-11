from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_detail import VmDetail


T = TypeVar("T", bound="GetVirtualMachineResponse200")


@_attrs_define
class GetVirtualMachineResponse200:
    """
    Attributes:
        data (VmDetail): Detailed operational and billing view of one owned VM service. Example: {'id': 353, 'hostname':
            'edge-app-01', 'os_user': 'debian', 'os_template': 'debian13-cloud', 'service_status': 'active',
            'provisioning_state': 'ready', 'bootstrap_completed_at': '2026-02-01T07:59:12+00:00', 'package': 'NVMe VPS -
            Standard', 'specs': {'cpu': 2, 'memory_mb': 4096, 'disk_gb': 80, 'bandwidth_gb': 4000, 'ipv4': 1, 'ipv6': 1},
            'ips': [{'ip': '23.182.128.79', 'cidr': '23.182.128.79/24', 'gateway': '23.182.128.1', 'type': 'v4'}],
            'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@laptop', 'pricing': {'term': 1, 'period': 'month',
            'price': '11.99', 'renew': '11.99', 'currency': 'USD'}, 'date_created': '2026-02-01T07:57:55+00:00',
            'date_renews': '2027-02-01T07:57:55+00:00', 'date_suspended': None, 'date_canceled': None}.
    """

    data: VmDetail
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_detail import VmDetail

        d = dict(src_dict)
        data = VmDetail.from_dict(d.pop("data"))

        get_virtual_machine_response_200 = cls(
            data=data,
        )

        get_virtual_machine_response_200.additional_properties = d
        return get_virtual_machine_response_200

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
