from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MintVmConsoleSessionBody")


@_attrs_define
class MintVmConsoleSessionBody:
    """
    Attributes:
        ttl (int | Unset): v2.4.0 (additive): requested session ttl in seconds, clamped to [5, 300]. Absent = the
            deployed default (30s). Note the PVE-side VNC ticket has its own upstream validity; open the console promptly.
    """

    ttl: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ttl = self.ttl

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ttl is not UNSET:
            field_dict["ttl"] = ttl

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ttl = d.pop("ttl", UNSET)

        mint_vm_console_session_body = cls(
            ttl=ttl,
        )

        mint_vm_console_session_body.additional_properties = d
        return mint_vm_console_session_body

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
