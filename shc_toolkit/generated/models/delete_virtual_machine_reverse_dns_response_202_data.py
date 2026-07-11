from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteVirtualMachineReverseDnsResponse202Data")


@_attrs_define
class DeleteVirtualMachineReverseDnsResponse202Data:
    """
    Attributes:
        service_id (int | Unset):
        ip (str | Unset):
        status (str | Unset):  Example: queued.
        job_id (int | Unset):
    """

    service_id: int | Unset = UNSET
    ip: str | Unset = UNSET
    status: str | Unset = UNSET
    job_id: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        ip = self.ip

        status = self.status

        job_id = self.job_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if service_id is not UNSET:
            field_dict["service_id"] = service_id
        if ip is not UNSET:
            field_dict["ip"] = ip
        if status is not UNSET:
            field_dict["status"] = status
        if job_id is not UNSET:
            field_dict["job_id"] = job_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id", UNSET)

        ip = d.pop("ip", UNSET)

        status = d.pop("status", UNSET)

        job_id = d.pop("job_id", UNSET)

        delete_virtual_machine_reverse_dns_response_202_data = cls(
            service_id=service_id,
            ip=ip,
            status=status,
            job_id=job_id,
        )

        delete_virtual_machine_reverse_dns_response_202_data.additional_properties = d
        return delete_virtual_machine_reverse_dns_response_202_data

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
