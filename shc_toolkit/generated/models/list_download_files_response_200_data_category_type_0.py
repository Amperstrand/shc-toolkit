from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ListDownloadFilesResponse200DataCategoryType0")


@_attrs_define
class ListDownloadFilesResponse200DataCategoryType0:
    """Selected category, or null when listing the root.

    Attributes:
        category_id (int):
        name (str):
        description (str):
        parent_id (int | None):
    """

    category_id: int
    name: str
    description: str
    parent_id: int | None

    def to_dict(self) -> dict[str, Any]:
        category_id = self.category_id

        name = self.name

        description = self.description

        parent_id: int | None
        parent_id = self.parent_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "category_id": category_id,
                "name": name,
                "description": description,
                "parent_id": parent_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        category_id = d.pop("category_id")

        name = d.pop("name")

        description = d.pop("description")

        def _parse_parent_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        list_download_files_response_200_data_category_type_0 = cls(
            category_id=category_id,
            name=name,
            description=description,
            parent_id=parent_id,
        )

        return list_download_files_response_200_data_category_type_0
