from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.proxmox_job import ProxmoxJob


T = TypeVar("T", bound="GetVirtualMachineJobResponse200")


@_attrs_define
class GetVirtualMachineJobResponse200:
    """
    Attributes:
        data (ProxmoxJob): Queued or historical background job for one owned VM service. Example: {'job_id': 912,
            'service_id': 353, 'type': 'backup', 'status': 'running', 'progress': 45, 'step': 'Creating backup archive',
            'error': None, 'requested': {'name': 'nightly-demo', 'mode': 'suspend', 'backup_id': None, 'storage': 'pbs'},
            'created_at': '2026-04-17T01:23:45+00:00', 'completed_at': None}.
    """

    data: ProxmoxJob
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
        from ..models.proxmox_job import ProxmoxJob

        d = dict(src_dict)
        data = ProxmoxJob.from_dict(d.pop("data"))

        get_virtual_machine_job_response_200 = cls(
            data=data,
        )

        get_virtual_machine_job_response_200.additional_properties = d
        return get_virtual_machine_job_response_200

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
