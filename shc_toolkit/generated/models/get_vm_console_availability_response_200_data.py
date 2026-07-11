from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetVmConsoleAvailabilityResponse200Data")


@_attrs_define
class GetVmConsoleAvailabilityResponse200Data:
    """
    Attributes:
        service_id (int):
        available (bool):
        console_enabled (bool):
        host_eligible (bool):
        service_active (bool):
    """

    service_id: int
    available: bool
    console_enabled: bool
    host_eligible: bool
    service_active: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        available = self.available

        console_enabled = self.console_enabled

        host_eligible = self.host_eligible

        service_active = self.service_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "available": available,
                "console_enabled": console_enabled,
                "host_eligible": host_eligible,
                "service_active": service_active,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        available = d.pop("available")

        console_enabled = d.pop("console_enabled")

        host_eligible = d.pop("host_eligible")

        service_active = d.pop("service_active")

        get_vm_console_availability_response_200_data = cls(
            service_id=service_id,
            available=available,
            console_enabled=console_enabled,
            host_eligible=host_eligible,
            service_active=service_active,
        )

        get_vm_console_availability_response_200_data.additional_properties = d
        return get_vm_console_availability_response_200_data

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
