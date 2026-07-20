from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.list_download_files_response_200_data_categories_item import (
        ListDownloadFilesResponse200DataCategoriesItem,
    )
    from ..models.list_download_files_response_200_data_category_type_0 import (
        ListDownloadFilesResponse200DataCategoryType0,
    )
    from ..models.list_download_files_response_200_data_files_item import (
        ListDownloadFilesResponse200DataFilesItem,
    )
    from ..models.list_download_files_response_200_data_parent_category_type_0 import (
        ListDownloadFilesResponse200DataParentCategoryType0,
    )


T = TypeVar("T", bound="ListDownloadFilesResponse200Data")


@_attrs_define
class ListDownloadFilesResponse200Data:
    """
    Attributes:
        category (ListDownloadFilesResponse200DataCategoryType0 | None): Selected category, or null when listing the
            root.
        parent_category (ListDownloadFilesResponse200DataParentCategoryType0 | None): Parent category of the selected
            category, or null when absent.
        categories (list[ListDownloadFilesResponse200DataCategoriesItem]): Child categories visible at this level.
        files (list[ListDownloadFilesResponse200DataFilesItem]): Download files available to the authenticated client at
            this level.
        total_files (int): Portal-parity total files in the category for the company, not entitlement-filtered.
    """

    category: ListDownloadFilesResponse200DataCategoryType0 | None
    parent_category: ListDownloadFilesResponse200DataParentCategoryType0 | None
    categories: list[ListDownloadFilesResponse200DataCategoriesItem]
    files: list[ListDownloadFilesResponse200DataFilesItem]
    total_files: int

    def to_dict(self) -> dict[str, Any]:
        from ..models.list_download_files_response_200_data_category_type_0 import (
            ListDownloadFilesResponse200DataCategoryType0,
        )
        from ..models.list_download_files_response_200_data_parent_category_type_0 import (
            ListDownloadFilesResponse200DataParentCategoryType0,
        )

        category: dict[str, Any] | None
        if isinstance(self.category, ListDownloadFilesResponse200DataCategoryType0):
            category = self.category.to_dict()
        else:
            category = self.category

        parent_category: dict[str, Any] | None
        if isinstance(
            self.parent_category, ListDownloadFilesResponse200DataParentCategoryType0
        ):
            parent_category = self.parent_category.to_dict()
        else:
            parent_category = self.parent_category

        categories = []
        for categories_item_data in self.categories:
            categories_item = categories_item_data.to_dict()
            categories.append(categories_item)

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        total_files = self.total_files

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "category": category,
                "parent_category": parent_category,
                "categories": categories,
                "files": files,
                "total_files": total_files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_download_files_response_200_data_categories_item import (
            ListDownloadFilesResponse200DataCategoriesItem,
        )
        from ..models.list_download_files_response_200_data_category_type_0 import (
            ListDownloadFilesResponse200DataCategoryType0,
        )
        from ..models.list_download_files_response_200_data_files_item import (
            ListDownloadFilesResponse200DataFilesItem,
        )
        from ..models.list_download_files_response_200_data_parent_category_type_0 import (
            ListDownloadFilesResponse200DataParentCategoryType0,
        )

        d = dict(src_dict)

        def _parse_category(
            data: object,
        ) -> ListDownloadFilesResponse200DataCategoryType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                category_type_0 = (
                    ListDownloadFilesResponse200DataCategoryType0.from_dict(data)
                )

                return category_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ListDownloadFilesResponse200DataCategoryType0 | None, data)

        category = _parse_category(d.pop("category"))

        def _parse_parent_category(
            data: object,
        ) -> ListDownloadFilesResponse200DataParentCategoryType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_category_type_0 = (
                    ListDownloadFilesResponse200DataParentCategoryType0.from_dict(data)
                )

                return parent_category_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                ListDownloadFilesResponse200DataParentCategoryType0 | None, data
            )

        parent_category = _parse_parent_category(d.pop("parent_category"))

        categories = []
        _categories = d.pop("categories")
        for categories_item_data in _categories:
            categories_item = ListDownloadFilesResponse200DataCategoriesItem.from_dict(
                categories_item_data
            )

            categories.append(categories_item)

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = ListDownloadFilesResponse200DataFilesItem.from_dict(
                files_item_data
            )

            files.append(files_item)

        total_files = d.pop("total_files")

        list_download_files_response_200_data = cls(
            category=category,
            parent_category=parent_category,
            categories=categories,
            files=files,
            total_files=total_files,
        )

        return list_download_files_response_200_data
