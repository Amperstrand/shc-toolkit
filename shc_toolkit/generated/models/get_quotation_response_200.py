from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.get_quotation_response_200_data import GetQuotationResponse200Data


T = TypeVar("T", bound="GetQuotationResponse200")


@_attrs_define
class GetQuotationResponse200:
    """
    Attributes:
        data (GetQuotationResponse200Data):
    """

    data: GetQuotationResponse200Data

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
        from ..models.get_quotation_response_200_data import GetQuotationResponse200Data

        d = dict(src_dict)
        data = GetQuotationResponse200Data.from_dict(d.pop("data"))

        get_quotation_response_200 = cls(
            data=data,
        )

        return get_quotation_response_200
