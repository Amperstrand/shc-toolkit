from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmSshKeyDeleteLiveRequest")


@_attrs_define
class VmSshKeyDeleteLiveRequest:
    """Live-remove an SSH key from the running VM by fingerprint, and scrub it from the persisted set.

    Example:
        {'key_fingerprint': 'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}

    Attributes:
        key_fingerprint (str): Fingerprint of the key to remove. `SHA256:` and `MD5:` forms are accepted. Example:
            SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU.
    """

    key_fingerprint: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key_fingerprint = self.key_fingerprint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key_fingerprint": key_fingerprint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key_fingerprint = d.pop("key_fingerprint")

        vm_ssh_key_delete_live_request = cls(
            key_fingerprint=key_fingerprint,
        )

        vm_ssh_key_delete_live_request.additional_properties = d
        return vm_ssh_key_delete_live_request

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
