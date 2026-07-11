from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delete_virtual_machine_reverse_dns_response_202_data import (
        DeleteVirtualMachineReverseDnsResponse202Data,
    )


T = TypeVar("T", bound="DeleteVirtualMachineReverseDnsResponse202")


@_attrs_define
class DeleteVirtualMachineReverseDnsResponse202:
    """
    Attributes:
        data (DeleteVirtualMachineReverseDnsResponse202Data):
    """

    data: DeleteVirtualMachineReverseDnsResponse202Data
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
        from ..models.delete_virtual_machine_reverse_dns_response_202_data import (
            DeleteVirtualMachineReverseDnsResponse202Data,
        )

        d = dict(src_dict)
        data = DeleteVirtualMachineReverseDnsResponse202Data.from_dict(d.pop("data"))

        delete_virtual_machine_reverse_dns_response_202 = cls(
            data=data,
        )

        delete_virtual_machine_reverse_dns_response_202.additional_properties = d
        return delete_virtual_machine_reverse_dns_response_202

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
