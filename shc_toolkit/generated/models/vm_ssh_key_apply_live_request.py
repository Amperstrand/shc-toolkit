from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmSshKeyApplyLiveRequest")


@_attrs_define
class VmSshKeyApplyLiveRequest:
    """Live-inject a single-line SSH public key into the running VM via the guest agent. The key is also persisted so a
    later reinstall keeps it.

        Example:
            {'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}

        Attributes:
            ssh_key (str): Single-line ssh-rsa, ssh-ed25519, or ecdsa-sha2-nistp256/384/521 public key. Example: ssh-ed25519
                AAAAC3NzaC1lZDI1NTE5AAAA... user@host.
    """

    ssh_key: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ssh_key = self.ssh_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ssh_key": ssh_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ssh_key = d.pop("ssh_key")

        vm_ssh_key_apply_live_request = cls(
            ssh_key=ssh_key,
        )

        vm_ssh_key_apply_live_request.additional_properties = d
        return vm_ssh_key_apply_live_request

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
