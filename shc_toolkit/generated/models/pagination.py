from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="Pagination")


@_attrs_define
class Pagination:
    """
    Example:
        {'total': 42, 'limit': 100, 'offset': 0, 'has_more': False}

    Attributes:
        total (int):  Example: 42.
        limit (int):  Example: 100.
        offset (int):
        has_more (bool):
    """

    total: int
    limit: int
    offset: int
    has_more: bool

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        limit = self.limit

        offset = self.offset

        has_more = self.has_more

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": has_more,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total = d.pop("total")

        limit = d.pop("limit")

        offset = d.pop("offset")

        has_more = d.pop("has_more")

        pagination = cls(
            total=total,
            limit=limit,
            offset=offset,
            has_more=has_more,
        )

        return pagination
