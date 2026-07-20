from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ListDownloadFilesResponse200DataCategoriesItem")


@_attrs_define
class ListDownloadFilesResponse200DataCategoriesItem:
    """
    Attributes:
        category_id (int):
        name (str):
        description (str):
    """

    category_id: int
    name: str
    description: str

    def to_dict(self) -> dict[str, Any]:
        category_id = self.category_id

        name = self.name

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "category_id": category_id,
                "name": name,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        category_id = d.pop("category_id")

        name = d.pop("name")

        description = d.pop("description")

        list_download_files_response_200_data_categories_item = cls(
            category_id=category_id,
            name=name,
            description=description,
        )

        return list_download_files_response_200_data_categories_item
