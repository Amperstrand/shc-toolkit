from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.get_kb_article_response_200_data import GetKbArticleResponse200Data


T = TypeVar("T", bound="GetKbArticleResponse200")


@_attrs_define
class GetKbArticleResponse200:
    """
    Attributes:
        data (GetKbArticleResponse200Data):
    """

    data: GetKbArticleResponse200Data

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
        from ..models.get_kb_article_response_200_data import (
            GetKbArticleResponse200Data,
        )

        d = dict(src_dict)
        data = GetKbArticleResponse200Data.from_dict(d.pop("data"))

        get_kb_article_response_200 = cls(
            data=data,
        )

        return get_kb_article_response_200
