from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.console_session_response import ConsoleSessionResponse


T = TypeVar("T", bound="MintVmConsoleSessionResponse201")


@_attrs_define
class MintVmConsoleSessionResponse201:
    """
    Attributes:
        data (ConsoleSessionResponse): A freshly minted, single-use noVNC console session. Open console_url in a browser
            before it expires.
    """

    data: ConsoleSessionResponse
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
        from ..models.console_session_response import ConsoleSessionResponse

        d = dict(src_dict)
        data = ConsoleSessionResponse.from_dict(d.pop("data"))

        mint_vm_console_session_response_201 = cls(
            data=data,
        )

        mint_vm_console_session_response_201.additional_properties = d
        return mint_vm_console_session_response_201

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
