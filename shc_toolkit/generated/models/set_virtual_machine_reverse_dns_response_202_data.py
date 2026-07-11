from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetVirtualMachineReverseDnsResponse202Data")


@_attrs_define
class SetVirtualMachineReverseDnsResponse202Data:
    """
    Attributes:
        service_id (int | Unset):
        ip (str | Unset):
        hostname (str | Unset):
        status (str | Unset):  Example: queued.
        job_id (int | Unset):
        pending_public (bool | Unset):
    """

    service_id: int | Unset = UNSET
    ip: str | Unset = UNSET
    hostname: str | Unset = UNSET
    status: str | Unset = UNSET
    job_id: int | Unset = UNSET
    pending_public: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        ip = self.ip

        hostname = self.hostname

        status = self.status

        job_id = self.job_id

        pending_public = self.pending_public

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if service_id is not UNSET:
            field_dict["service_id"] = service_id
        if ip is not UNSET:
            field_dict["ip"] = ip
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if status is not UNSET:
            field_dict["status"] = status
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if pending_public is not UNSET:
            field_dict["pending_public"] = pending_public

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id", UNSET)

        ip = d.pop("ip", UNSET)

        hostname = d.pop("hostname", UNSET)

        status = d.pop("status", UNSET)

        job_id = d.pop("job_id", UNSET)

        pending_public = d.pop("pending_public", UNSET)

        set_virtual_machine_reverse_dns_response_202_data = cls(
            service_id=service_id,
            ip=ip,
            hostname=hostname,
            status=status,
            job_id=job_id,
            pending_public=pending_public,
        )

        set_virtual_machine_reverse_dns_response_202_data.additional_properties = d
        return set_virtual_machine_reverse_dns_response_202_data

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
