from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.vm_network_interface import VmNetworkInterface


T = TypeVar("T", bound="GetVirtualMachineNetworkResponse200Data")


@_attrs_define
class GetVirtualMachineNetworkResponse200Data:
    """
    Attributes:
        service_id (int):  Example: 451.
        interfaces (list[VmNetworkInterface]):
    """

    service_id: int
    interfaces: list[VmNetworkInterface]

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        interfaces = []
        for interfaces_item_data in self.interfaces:
            interfaces_item = interfaces_item_data.to_dict()
            interfaces.append(interfaces_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "interfaces": interfaces,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_network_interface import VmNetworkInterface

        d = dict(src_dict)
        service_id = d.pop("service_id")

        interfaces = []
        _interfaces = d.pop("interfaces")
        for interfaces_item_data in _interfaces:
            interfaces_item = VmNetworkInterface.from_dict(interfaces_item_data)

            interfaces.append(interfaces_item)

        get_virtual_machine_network_response_200_data = cls(
            service_id=service_id,
            interfaces=interfaces,
        )

        return get_virtual_machine_network_response_200_data
