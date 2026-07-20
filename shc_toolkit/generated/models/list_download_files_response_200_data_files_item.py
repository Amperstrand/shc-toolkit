from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ListDownloadFilesResponse200DataFilesItem")


@_attrs_define
class ListDownloadFilesResponse200DataFilesItem:
    """
    Attributes:
        file_id (int):
        name (str):
        extension (str): File extension string supplied by the download manager model, or an empty string.
        category_id (int | None):
    """

    file_id: int
    name: str
    extension: str
    category_id: int | None

    def to_dict(self) -> dict[str, Any]:
        file_id = self.file_id

        name = self.name

        extension = self.extension

        category_id: int | None
        category_id = self.category_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "file_id": file_id,
                "name": name,
                "extension": extension,
                "category_id": category_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = d.pop("file_id")

        name = d.pop("name")

        extension = d.pop("extension")

        def _parse_category_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        category_id = _parse_category_id(d.pop("category_id"))

        list_download_files_response_200_data_files_item = cls(
            file_id=file_id,
            name=name,
            extension=extension,
            category_id=category_id,
        )

        return list_download_files_response_200_data_files_item
