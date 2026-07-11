from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.get_credit_handling_response_200_data import (
        GetCreditHandlingResponse200Data,
    )


T = TypeVar("T", bound="GetCreditHandlingResponse200")


@_attrs_define
class GetCreditHandlingResponse200:
    """
    Attributes:
        data (GetCreditHandlingResponse200Data):
    """

    data: GetCreditHandlingResponse200Data

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
        from ..models.get_credit_handling_response_200_data import (
            GetCreditHandlingResponse200Data,
        )

        d = dict(src_dict)
        data = GetCreditHandlingResponse200Data.from_dict(d.pop("data"))

        get_credit_handling_response_200 = cls(
            data=data,
        )

        return get_credit_handling_response_200
