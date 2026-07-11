from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_virtual_machine_reverse_dns_response_200_data_records_item import (
        GetVirtualMachineReverseDnsResponse200DataRecordsItem,
    )


T = TypeVar("T", bound="GetVirtualMachineReverseDnsResponse200Data")


@_attrs_define
class GetVirtualMachineReverseDnsResponse200Data:
    """
    Attributes:
        service_id (int | Unset):
        records (list[GetVirtualMachineReverseDnsResponse200DataRecordsItem] | Unset):
    """

    service_id: int | Unset = UNSET
    records: list[GetVirtualMachineReverseDnsResponse200DataRecordsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        records: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.records, Unset):
            records = []
            for records_item_data in self.records:
                records_item = records_item_data.to_dict()
                records.append(records_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if service_id is not UNSET:
            field_dict["service_id"] = service_id
        if records is not UNSET:
            field_dict["records"] = records

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_virtual_machine_reverse_dns_response_200_data_records_item import (
            GetVirtualMachineReverseDnsResponse200DataRecordsItem,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id", UNSET)

        _records = d.pop("records", UNSET)
        records: list[GetVirtualMachineReverseDnsResponse200DataRecordsItem] | Unset = (
            UNSET
        )
        if _records is not UNSET:
            records = []
            for records_item_data in _records:
                records_item = (
                    GetVirtualMachineReverseDnsResponse200DataRecordsItem.from_dict(
                        records_item_data
                    )
                )

                records.append(records_item)

        get_virtual_machine_reverse_dns_response_200_data = cls(
            service_id=service_id,
            records=records,
        )

        get_virtual_machine_reverse_dns_response_200_data.additional_properties = d
        return get_virtual_machine_reverse_dns_response_200_data

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
