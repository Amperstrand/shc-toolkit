from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.register_response_data import RegisterResponseData


T = TypeVar("T", bound="RegisterResponse")


@_attrs_define
class RegisterResponse:
    """
    Attributes:
        data (RegisterResponseData):
    """

    data: RegisterResponseData

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.register_response_data import RegisterResponseData

        d = dict(src_dict)
        data = RegisterResponseData.from_dict(d.pop("data"))

        register_response = cls(
            data=data,
        )

        return register_response
