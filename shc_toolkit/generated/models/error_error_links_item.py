from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.error_error_links_item_rel import (
    ErrorErrorLinksItemRel,
    check_error_error_links_item_rel,
)

T = TypeVar("T", bound="ErrorErrorLinksItem")


@_attrs_define
class ErrorErrorLinksItem:
    rel: ErrorErrorLinksItemRel
    href: str

    def to_dict(self) -> dict[str, Any]:
        rel: str = self.rel

        href = self.href

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "rel": rel,
                "href": href,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        rel = check_error_error_links_item_rel(d.pop("rel"))

        href = d.pop("href")

        error_error_links_item = cls(
            rel=rel,
            href=href,
        )

        return error_error_links_item
