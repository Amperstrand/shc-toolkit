from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.list_kb_categories_response_200_data import (
        ListKbCategoriesResponse200Data,
    )


T = TypeVar("T", bound="ListKbCategoriesResponse200")


@_attrs_define
class ListKbCategoriesResponse200:
    data: ListKbCategoriesResponse200Data

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
        from ..models.list_kb_categories_response_200_data import (
            ListKbCategoriesResponse200Data,
        )

        d = dict(src_dict)
        data = ListKbCategoriesResponse200Data.from_dict(d.pop("data"))

        list_kb_categories_response_200 = cls(
            data=data,
        )

        return list_kb_categories_response_200
