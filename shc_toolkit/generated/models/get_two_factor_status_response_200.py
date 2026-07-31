from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.get_two_factor_status_response_200_data import (
        GetTwoFactorStatusResponse200Data,
    )


T = TypeVar("T", bound="GetTwoFactorStatusResponse200")


@_attrs_define
class GetTwoFactorStatusResponse200:
    data: GetTwoFactorStatusResponse200Data

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
        from ..models.get_two_factor_status_response_200_data import (
            GetTwoFactorStatusResponse200Data,
        )

        d = dict(src_dict)
        data = GetTwoFactorStatusResponse200Data.from_dict(d.pop("data"))

        get_two_factor_status_response_200 = cls(
            data=data,
        )

        return get_two_factor_status_response_200
