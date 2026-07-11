from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.get_kb_article_response_200_data_content_type_type_1 import (
    GetKbArticleResponse200DataContentTypeType1,
)
from ..models.get_kb_article_response_200_data_content_type_type_2_type_1 import (
    GetKbArticleResponse200DataContentTypeType2Type1,
)
from ..models.get_kb_article_response_200_data_content_type_type_3_type_1 import (
    GetKbArticleResponse200DataContentTypeType3Type1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_kb_article_response_200_data_categories_item import (
        GetKbArticleResponse200DataCategoriesItem,
    )


T = TypeVar("T", bound="GetKbArticleResponse200Data")


@_attrs_define
class GetKbArticleResponse200Data:
    """
    Attributes:
        id (int):  Example: 21.
        title (None | str):  Example: How to reboot a VM.
        content (None | str):
        categories (list[GetKbArticleResponse200DataCategoriesItem]):
        up_votes (int):  Example: 12.
        down_votes (int):  Example: 1.
        content_type (GetKbArticleResponse200DataContentTypeType1 | GetKbArticleResponse200DataContentTypeType2Type1 |
            GetKbArticleResponse200DataContentTypeType3Type1 | None | Unset):  Example: html.
    """

    id: int
    title: None | str
    content: None | str
    categories: list[GetKbArticleResponse200DataCategoriesItem]
    up_votes: int
    down_votes: int
    content_type: (
        GetKbArticleResponse200DataContentTypeType1
        | GetKbArticleResponse200DataContentTypeType2Type1
        | GetKbArticleResponse200DataContentTypeType3Type1
        | None
        | Unset
    ) = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title: None | str
        title = self.title

        content: None | str
        content = self.content

        categories = []
        for categories_item_data in self.categories:
            categories_item = categories_item_data.to_dict()
            categories.append(categories_item)

        up_votes = self.up_votes

        down_votes = self.down_votes

        content_type: None | str | Unset
        if isinstance(self.content_type, Unset):
            content_type = UNSET
        elif isinstance(self.content_type, GetKbArticleResponse200DataContentTypeType1):
            content_type = self.content_type.value
        elif isinstance(
            self.content_type, GetKbArticleResponse200DataContentTypeType2Type1
        ):
            content_type = self.content_type.value
        elif isinstance(
            self.content_type, GetKbArticleResponse200DataContentTypeType3Type1
        ):
            content_type = self.content_type.value
        else:
            content_type = self.content_type

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "title": title,
                "content": content,
                "categories": categories,
                "up_votes": up_votes,
                "down_votes": down_votes,
            }
        )
        if content_type is not UNSET:
            field_dict["content_type"] = content_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_kb_article_response_200_data_categories_item import (
            GetKbArticleResponse200DataCategoriesItem,
        )

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))

        def _parse_content(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        content = _parse_content(d.pop("content"))

        categories = []
        _categories = d.pop("categories")
        for categories_item_data in _categories:
            categories_item = GetKbArticleResponse200DataCategoriesItem.from_dict(
                categories_item_data
            )

            categories.append(categories_item)

        up_votes = d.pop("up_votes")

        down_votes = d.pop("down_votes")

        def _parse_content_type(
            data: object,
        ) -> (
            GetKbArticleResponse200DataContentTypeType1
            | GetKbArticleResponse200DataContentTypeType2Type1
            | GetKbArticleResponse200DataContentTypeType3Type1
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                content_type_type_1 = GetKbArticleResponse200DataContentTypeType1(data)

                return content_type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                content_type_type_2_type_1 = (
                    GetKbArticleResponse200DataContentTypeType2Type1(data)
                )

                return content_type_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                content_type_type_3_type_1 = (
                    GetKbArticleResponse200DataContentTypeType3Type1(data)
                )

                return content_type_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                GetKbArticleResponse200DataContentTypeType1
                | GetKbArticleResponse200DataContentTypeType2Type1
                | GetKbArticleResponse200DataContentTypeType3Type1
                | None
                | Unset,
                data,
            )

        content_type = _parse_content_type(d.pop("content_type", UNSET))

        get_kb_article_response_200_data = cls(
            id=id,
            title=title,
            content=content,
            categories=categories,
            up_votes=up_votes,
            down_votes=down_votes,
            content_type=content_type,
        )

        return get_kb_article_response_200_data
