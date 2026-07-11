from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ManagedAccountReleaseResponse")


@_attrs_define
class ManagedAccountReleaseResponse:
    """
    Attributes:
        released (bool):  Example: True.
        managed_client_id (int):  Example: 4096.
    """

    released: bool
    managed_client_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        released = self.released

        managed_client_id = self.managed_client_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "released": released,
                "managed_client_id": managed_client_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        released = d.pop("released")

        managed_client_id = d.pop("managed_client_id")

        managed_account_release_response = cls(
            released=released,
            managed_client_id=managed_client_id,
        )

        managed_account_release_response.additional_properties = d
        return managed_account_release_response

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
