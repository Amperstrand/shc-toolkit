from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SetSshKeyRequest")


@_attrs_define
class SetSshKeyRequest:
    """
    Example:
        {'service_id': 353, 'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}

    Attributes:
        service_id (int):  Example: 353.
        ssh_key (str): Single-line ssh-rsa, ssh-ed25519, or ecdsa-sha2-nistp256/384/521 public key. Example: ssh-ed25519
            AAAAC3NzaC1lZDI1NTE5AAAA... user@host.
    """

    service_id: int
    ssh_key: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        ssh_key = self.ssh_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "ssh_key": ssh_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        ssh_key = d.pop("ssh_key")

        set_ssh_key_request = cls(
            service_id=service_id,
            ssh_key=ssh_key,
        )

        set_ssh_key_request.additional_properties = d
        return set_ssh_key_request

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
