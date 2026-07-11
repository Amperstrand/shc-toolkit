from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.list_support_tickets_response_200_items_item_priority import (
    ListSupportTicketsResponse200ItemsItemPriority,
)
from ..models.list_support_tickets_response_200_items_item_status import (
    ListSupportTicketsResponse200ItemsItemStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListSupportTicketsResponse200ItemsItem")


@_attrs_define
class ListSupportTicketsResponse200ItemsItem:
    """
    Attributes:
        id (int):  Example: 501.
        code (str):  Example: ABC-123456.
        department_id (int):  Example: 3.
        summary (None | str):  Example: Cannot reach VM.
        priority (ListSupportTicketsResponse200ItemsItemPriority):  Example: medium.
        status (ListSupportTicketsResponse200ItemsItemStatus):  Example: open.
        replies_count (int):  Example: 4.
        last_reply_date (datetime.datetime | None | Unset):
        date_added (datetime.datetime | None | Unset):
        date_updated (datetime.datetime | None | Unset):
    """

    id: int
    code: str
    department_id: int
    summary: None | str
    priority: ListSupportTicketsResponse200ItemsItemPriority
    status: ListSupportTicketsResponse200ItemsItemStatus
    replies_count: int
    last_reply_date: datetime.datetime | None | Unset = UNSET
    date_added: datetime.datetime | None | Unset = UNSET
    date_updated: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        code = self.code

        department_id = self.department_id

        summary: None | str
        summary = self.summary

        priority = self.priority.value

        status = self.status.value

        replies_count = self.replies_count

        last_reply_date: None | str | Unset
        if isinstance(self.last_reply_date, Unset):
            last_reply_date = UNSET
        elif isinstance(self.last_reply_date, datetime.datetime):
            last_reply_date = self.last_reply_date.isoformat()
        else:
            last_reply_date = self.last_reply_date

        date_added: None | str | Unset
        if isinstance(self.date_added, Unset):
            date_added = UNSET
        elif isinstance(self.date_added, datetime.datetime):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        date_updated: None | str | Unset
        if isinstance(self.date_updated, Unset):
            date_updated = UNSET
        elif isinstance(self.date_updated, datetime.datetime):
            date_updated = self.date_updated.isoformat()
        else:
            date_updated = self.date_updated

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "code": code,
                "department_id": department_id,
                "summary": summary,
                "priority": priority,
                "status": status,
                "replies_count": replies_count,
            }
        )
        if last_reply_date is not UNSET:
            field_dict["last_reply_date"] = last_reply_date
        if date_added is not UNSET:
            field_dict["date_added"] = date_added
        if date_updated is not UNSET:
            field_dict["date_updated"] = date_updated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        code = d.pop("code")

        department_id = d.pop("department_id")

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        priority = ListSupportTicketsResponse200ItemsItemPriority(d.pop("priority"))

        status = ListSupportTicketsResponse200ItemsItemStatus(d.pop("status"))

        replies_count = d.pop("replies_count")

        def _parse_last_reply_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_reply_date_type_0 = datetime.datetime.fromisoformat(data)

                return last_reply_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_reply_date = _parse_last_reply_date(d.pop("last_reply_date", UNSET))

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

        def _parse_date_updated(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_updated_type_0 = datetime.datetime.fromisoformat(data)

                return date_updated_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_updated = _parse_date_updated(d.pop("date_updated", UNSET))

        list_support_tickets_response_200_items_item = cls(
            id=id,
            code=code,
            department_id=department_id,
            summary=summary,
            priority=priority,
            status=status,
            replies_count=replies_count,
            last_reply_date=last_reply_date,
            date_added=date_added,
            date_updated=date_updated,
        )

        return list_support_tickets_response_200_items_item
