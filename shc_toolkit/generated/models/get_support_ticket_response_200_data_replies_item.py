from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.get_support_ticket_response_200_data_replies_item_author_type import (
    GetSupportTicketResponse200DataRepliesItemAuthorType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSupportTicketResponse200DataRepliesItem")


@_attrs_define
class GetSupportTicketResponse200DataRepliesItem:
    """
    Attributes:
        id (int):  Example: 9001.
        author_type (GetSupportTicketResponse200DataRepliesItemAuthorType):  Example: client.
        details (None | str):
        author_name (None | str | Unset):  Example: Jane Roe.
        date_added (datetime.datetime | None | Unset):
    """

    id: int
    author_type: GetSupportTicketResponse200DataRepliesItemAuthorType
    details: None | str
    author_name: None | str | Unset = UNSET
    date_added: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        author_type = self.author_type.value

        details: None | str
        details = self.details

        author_name: None | str | Unset
        if isinstance(self.author_name, Unset):
            author_name = UNSET
        else:
            author_name = self.author_name

        date_added: None | str | Unset
        if isinstance(self.date_added, Unset):
            date_added = UNSET
        elif isinstance(self.date_added, datetime.datetime):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "author_type": author_type,
                "details": details,
            }
        )
        if author_name is not UNSET:
            field_dict["author_name"] = author_name
        if date_added is not UNSET:
            field_dict["date_added"] = date_added

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        author_type = GetSupportTicketResponse200DataRepliesItemAuthorType(
            d.pop("author_type")
        )

        def _parse_details(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        details = _parse_details(d.pop("details"))

        def _parse_author_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        author_name = _parse_author_name(d.pop("author_name", UNSET))

        def _parse_date_added(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_added_type_0 = datetime.datetime.fromisoformat(data)

                return date_added_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_added = _parse_date_added(d.pop("date_added", UNSET))

        get_support_ticket_response_200_data_replies_item = cls(
            id=id,
            author_type=author_type,
            details=details,
            author_name=author_name,
            date_added=date_added,
        )

        return get_support_ticket_response_200_data_replies_item
