from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SetVirtualMachineReverseDnsBody")


@_attrs_define
class SetVirtualMachineReverseDnsBody:
    """
    Example:
        {'ip': '203.0.113.45', 'hostname': 'vm42.customer.example.com'}

    Attributes:
        ip (str): An IP assigned to this VM, inside a managed reverse zone.
        hostname (str): FQDN that already A/AAAA-resolves back to ip (FCrDNS).
    """

    ip: str
    hostname: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ip = self.ip

        hostname = self.hostname

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ip": ip,
                "hostname": hostname,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ip = d.pop("ip")

        hostname = d.pop("hostname")

        set_virtual_machine_reverse_dns_body = cls(
            ip=ip,
            hostname=hostname,
        )

        set_virtual_machine_reverse_dns_body.additional_properties = d
        return set_virtual_machine_reverse_dns_body

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
