from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="VmNetworkInterface")


@_attrs_define
class VmNetworkInterface:
    device: None | str
    mac: None | str
    ip: None | str
    ip6: None | str
    gateway: None | str
    gateway6: None | str
    rate: None | str
    """ Shaping rate in Mbit, or null when unshaped. """

    def to_dict(self) -> dict[str, Any]:
        device: None | str
        device = self.device

        mac: None | str
        mac = self.mac

        ip: None | str
        ip = self.ip

        ip6: None | str
        ip6 = self.ip6

        gateway: None | str
        gateway = self.gateway

        gateway6: None | str
        gateway6 = self.gateway6

        rate: None | str
        rate = self.rate

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "device": device,
                "mac": mac,
                "ip": ip,
                "ip6": ip6,
                "gateway": gateway,
                "gateway6": gateway6,
                "rate": rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_device(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        device = _parse_device(d.pop("device"))

        def _parse_mac(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        mac = _parse_mac(d.pop("mac"))

        def _parse_ip(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        ip = _parse_ip(d.pop("ip"))

        def _parse_ip6(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        ip6 = _parse_ip6(d.pop("ip6"))

        def _parse_gateway(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gateway = _parse_gateway(d.pop("gateway"))

        def _parse_gateway6(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gateway6 = _parse_gateway6(d.pop("gateway6"))

        def _parse_rate(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rate = _parse_rate(d.pop("rate"))

        vm_network_interface = cls(
            device=device,
            mac=mac,
            ip=ip,
            ip6=ip6,
            gateway=gateway,
            gateway6=gateway6,
            rate=rate,
        )

        return vm_network_interface
