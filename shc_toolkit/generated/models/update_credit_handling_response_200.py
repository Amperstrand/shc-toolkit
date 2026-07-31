from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.update_credit_handling_response_200_data import (
        UpdateCreditHandlingResponse200Data,
    )


T = TypeVar("T", bound="UpdateCreditHandlingResponse200")


@_attrs_define
class UpdateCreditHandlingResponse200:
    data: UpdateCreditHandlingResponse200Data

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
        from ..models.update_credit_handling_response_200_data import (
            UpdateCreditHandlingResponse200Data,
        )

        d = dict(src_dict)
        data = UpdateCreditHandlingResponse200Data.from_dict(d.pop("data"))

        update_credit_handling_response_200 = cls(
            data=data,
        )

        return update_credit_handling_response_200
