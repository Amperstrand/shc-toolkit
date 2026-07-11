from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ip_address_type import IpAddressType

T = TypeVar("T", bound="IpAddress")


@_attrs_define
class IpAddress:
    """Assigned IP address currently associated with an owned VM service.

    Attributes:
        ip (str):  Example: 23.182.128.79.
        cidr (str):  Example: 23.182.128.79/24.
        gateway (None | str):  Example: 23.182.128.1.
        type_ (IpAddressType):  Example: v4.
    """

    ip: str
    cidr: str
    gateway: None | str
    type_: IpAddressType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ip = self.ip

        cidr = self.cidr

        gateway: None | str
        gateway = self.gateway

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ip": ip,
                "cidr": cidr,
                "gateway": gateway,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ip = d.pop("ip")

        cidr = d.pop("cidr")

        def _parse_gateway(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gateway = _parse_gateway(d.pop("gateway"))

        type_ = IpAddressType(d.pop("type"))

        ip_address = cls(
            ip=ip,
            cidr=cidr,
            gateway=gateway,
            type_=type_,
        )

        ip_address.additional_properties = d
        return ip_address

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
