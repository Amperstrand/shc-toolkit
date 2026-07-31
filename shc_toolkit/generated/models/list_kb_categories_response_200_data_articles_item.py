from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="ListKbCategoriesResponse200DataArticlesItem")


@_attrs_define
class ListKbCategoriesResponse200DataArticlesItem:
    id: int
    title: None | str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title: None | str
        title = self.title

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "title": title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))

        list_kb_categories_response_200_data_articles_item = cls(
            id=id,
            title=title,
        )

        return list_kb_categories_response_200_data_articles_item
