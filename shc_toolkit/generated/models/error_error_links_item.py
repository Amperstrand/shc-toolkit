from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.error_error_links_item_rel import ErrorErrorLinksItemRel

T = TypeVar("T", bound="ErrorErrorLinksItem")


@_attrs_define
class ErrorErrorLinksItem:
    """
    Attributes:
        rel (ErrorErrorLinksItemRel):  Example: status.
        href (str):  Example: /user-api/v2/vm/353/summary.
    """

    rel: ErrorErrorLinksItemRel
    href: str

    def to_dict(self) -> dict[str, Any]:
        rel = self.rel.value

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rel = ErrorErrorLinksItemRel(d.pop("rel"))

        href = d.pop("href")

        error_error_links_item = cls(
            rel=rel,
            href=href,
        )

        return error_error_links_item
