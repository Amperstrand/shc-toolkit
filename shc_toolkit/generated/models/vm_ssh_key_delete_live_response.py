from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmSshKeyDeleteLiveResponse")


@_attrs_define
class VmSshKeyDeleteLiveResponse:
    """Result of a live SSH-key removal. Idempotent: `removed` is false when the fingerprint was not present.

    Attributes:
        service_id (int):  Example: 353.
        removed (bool):  Example: True.
    """

    service_id: int
    removed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        removed = self.removed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "removed": removed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        removed = d.pop("removed")

        vm_ssh_key_delete_live_response = cls(
            service_id=service_id,
            removed=removed,
        )

        vm_ssh_key_delete_live_response.additional_properties = d
        return vm_ssh_key_delete_live_response

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
