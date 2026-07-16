from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="DocumentListItem")


@_attrs_define
class DocumentListItem:
    """
    Attributes:
        document_id (int):
        name (str):
        description (str):
        extension (str):
        date_added (None | str): Blesta UTC timestamp as emitted by the v2 handler. Example: 2026-07-12 02:50:55.
    """

    document_id: int
    name: str
    description: str
    extension: str
    date_added: None | str

    def to_dict(self) -> dict[str, Any]:
        document_id = self.document_id

        name = self.name

        description = self.description

        extension = self.extension

        date_added: None | str
        date_added = self.date_added

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "document_id": document_id,
                "name": name,
                "description": description,
                "extension": extension,
                "date_added": date_added,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        document_id = d.pop("document_id")

        name = d.pop("name")

        description = d.pop("description")

        extension = d.pop("extension")

        def _parse_date_added(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        date_added = _parse_date_added(d.pop("date_added"))

        document_list_item = cls(
            document_id=document_id,
            name=name,
            description=description,
            extension=extension,
            date_added=date_added,
        )

        return document_list_item
