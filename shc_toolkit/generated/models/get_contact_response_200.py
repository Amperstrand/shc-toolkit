from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.get_contact_response_200_data import GetContactResponse200Data


T = TypeVar("T", bound="GetContactResponse200")


@_attrs_define
class GetContactResponse200:
    data: GetContactResponse200Data

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.get_contact_response_200_data import GetContactResponse200Data

        d = dict(src_dict)
        data = GetContactResponse200Data.from_dict(d.pop("data"))

        get_contact_response_200 = cls(
            data=data,
        )

        return get_contact_response_200
