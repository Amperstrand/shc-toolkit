from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_kb_categories_response_200_data_articles_item import (
        ListKbCategoriesResponse200DataArticlesItem,
    )
    from ..models.list_kb_categories_response_200_data_categories_item import (
        ListKbCategoriesResponse200DataCategoriesItem,
    )


T = TypeVar("T", bound="ListKbCategoriesResponse200Data")


@_attrs_define
class ListKbCategoriesResponse200Data:
    """
    Attributes:
        category_id (int | None):
        categories (list[ListKbCategoriesResponse200DataCategoriesItem]):
        articles (list[ListKbCategoriesResponse200DataArticlesItem]):
        article_limit (int | Unset): Page size applied to the articles list in this category. Example: 20.
        article_offset (int | Unset): Zero-based offset of the first returned article.
        article_total (int | Unset): Total number of articles visible to the client in this category. Example: 42.
        article_has_more (bool | Unset): True when more articles exist beyond this page. Example: True.
        article_next_offset (int | None | Unset): Offset to request the next page of articles, or null when
            article_has_more is false. Example: 20.
    """

    category_id: int | None
    categories: list[ListKbCategoriesResponse200DataCategoriesItem]
    articles: list[ListKbCategoriesResponse200DataArticlesItem]
    article_limit: int | Unset = UNSET
    article_offset: int | Unset = UNSET
    article_total: int | Unset = UNSET
    article_has_more: bool | Unset = UNSET
    article_next_offset: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        category_id: int | None
        category_id = self.category_id

        categories = []
        for categories_item_data in self.categories:
            categories_item = categories_item_data.to_dict()
            categories.append(categories_item)

        articles = []
        for articles_item_data in self.articles:
            articles_item = articles_item_data.to_dict()
            articles.append(articles_item)

        article_limit = self.article_limit

        article_offset = self.article_offset

        article_total = self.article_total

        article_has_more = self.article_has_more

        article_next_offset: int | None | Unset
        if isinstance(self.article_next_offset, Unset):
            article_next_offset = UNSET
        else:
            article_next_offset = self.article_next_offset

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "category_id": category_id,
                "categories": categories,
                "articles": articles,
            }
        )
        if article_limit is not UNSET:
            field_dict["article_limit"] = article_limit
        if article_offset is not UNSET:
            field_dict["article_offset"] = article_offset
        if article_total is not UNSET:
            field_dict["article_total"] = article_total
        if article_has_more is not UNSET:
            field_dict["article_has_more"] = article_has_more
        if article_next_offset is not UNSET:
            field_dict["article_next_offset"] = article_next_offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_kb_categories_response_200_data_articles_item import (
            ListKbCategoriesResponse200DataArticlesItem,
        )
        from ..models.list_kb_categories_response_200_data_categories_item import (
            ListKbCategoriesResponse200DataCategoriesItem,
        )

        d = dict(src_dict)

        def _parse_category_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        category_id = _parse_category_id(d.pop("category_id"))

        categories = []
        _categories = d.pop("categories")
        for categories_item_data in _categories:
            categories_item = ListKbCategoriesResponse200DataCategoriesItem.from_dict(
                categories_item_data
            )

            categories.append(categories_item)

        articles = []
        _articles = d.pop("articles")
        for articles_item_data in _articles:
            articles_item = ListKbCategoriesResponse200DataArticlesItem.from_dict(
                articles_item_data
            )

            articles.append(articles_item)

        article_limit = d.pop("article_limit", UNSET)

        article_offset = d.pop("article_offset", UNSET)

        article_total = d.pop("article_total", UNSET)

        article_has_more = d.pop("article_has_more", UNSET)

        def _parse_article_next_offset(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        article_next_offset = _parse_article_next_offset(
            d.pop("article_next_offset", UNSET)
        )

        list_kb_categories_response_200_data = cls(
            category_id=category_id,
            categories=categories,
            articles=articles,
            article_limit=article_limit,
            article_offset=article_offset,
            article_total=article_total,
            article_has_more=article_has_more,
            article_next_offset=article_next_offset,
        )

        return list_kb_categories_response_200_data
