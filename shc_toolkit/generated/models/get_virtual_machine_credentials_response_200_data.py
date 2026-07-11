from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetVirtualMachineCredentialsResponse200Data")


@_attrs_define
class GetVirtualMachineCredentialsResponse200Data:
    """
    Attributes:
        user (str): VM login username from Service Info (service_fields.user). Example: root.
        password (str): VM login password from Service Info (service_fields.password), decrypted.
    """

    user: str
    password: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user

        password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
                "password": password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user = d.pop("user")

        password = d.pop("password")

        get_virtual_machine_credentials_response_200_data = cls(
            user=user,
            password=password,
        )

        get_virtual_machine_credentials_response_200_data.additional_properties = d
        return get_virtual_machine_credentials_response_200_data

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
