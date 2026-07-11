from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SshKeyEntry")


@_attrs_define
class SshKeyEntry:
    """
    Example:
        {'service_id': 353, 'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host', 'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}

    Attributes:
        service_id (int):  Example: 353.
        ssh_key (str): The single-line public key. Multi-key historical values are split into one entry per line.
            Example: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host.
        key_fingerprint (None | str): Server-computed SHA-256 fingerprint in OpenSSH form (`SHA256:` + base64 with
            padding stripped). Pass this verbatim to `DELETE /ssh-key` to remove the entry. May be `null` for keys that fail
            to parse server-side. Example: SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU.
    """

    service_id: int
    ssh_key: str
    key_fingerprint: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        ssh_key = self.ssh_key

        key_fingerprint: None | str
        key_fingerprint = self.key_fingerprint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "ssh_key": ssh_key,
                "key_fingerprint": key_fingerprint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        ssh_key = d.pop("ssh_key")

        def _parse_key_fingerprint(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        key_fingerprint = _parse_key_fingerprint(d.pop("key_fingerprint"))

        ssh_key_entry = cls(
            service_id=service_id,
            ssh_key=ssh_key,
            key_fingerprint=key_fingerprint,
        )

        ssh_key_entry.additional_properties = d
        return ssh_key_entry

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
