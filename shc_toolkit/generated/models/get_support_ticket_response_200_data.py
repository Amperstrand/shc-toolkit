from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.get_support_ticket_response_200_data_priority import (
    GetSupportTicketResponse200DataPriority,
)
from ..models.get_support_ticket_response_200_data_status import (
    GetSupportTicketResponse200DataStatus,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_support_ticket_response_200_data_replies_item import (
        GetSupportTicketResponse200DataRepliesItem,
    )


T = TypeVar("T", bound="GetSupportTicketResponse200Data")


@_attrs_define
class GetSupportTicketResponse200Data:
    """
    Attributes:
        id (int):  Example: 501.
        code (str):  Example: ABC-123456.
        department_id (int):  Example: 3.
        summary (None | str):
        priority (GetSupportTicketResponse200DataPriority):
        status (GetSupportTicketResponse200DataStatus):
        replies (list[GetSupportTicketResponse200DataRepliesItem]):
        service_id (int | None | Unset):
        date_added (datetime.datetime | None | Unset):
        date_updated (datetime.datetime | None | Unset):
        date_closed (datetime.datetime | None | Unset):
        reply_limit (int | Unset):  Example: 100.
        reply_offset (int | Unset):
        reply_has_more (bool | Unset):
    """

    id: int
    code: str
    department_id: int
    summary: None | str
    priority: GetSupportTicketResponse200DataPriority
    status: GetSupportTicketResponse200DataStatus
    replies: list[GetSupportTicketResponse200DataRepliesItem]
    service_id: int | None | Unset = UNSET
    date_added: datetime.datetime | None | Unset = UNSET
    date_updated: datetime.datetime | None | Unset = UNSET
    date_closed: datetime.datetime | None | Unset = UNSET
    reply_limit: int | Unset = UNSET
    reply_offset: int | Unset = UNSET
    reply_has_more: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        code = self.code

        department_id = self.department_id

        summary: None | str
        summary = self.summary

        priority = self.priority.value

        status = self.status.value

        replies = []
        for replies_item_data in self.replies:
            replies_item = replies_item_data.to_dict()
            replies.append(replies_item)

        service_id: int | None | Unset
        if isinstance(self.service_id, Unset):
            service_id = UNSET
        else:
            service_id = self.service_id

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

        date_closed: None | str | Unset
        if isinstance(self.date_closed, Unset):
            date_closed = UNSET
        elif isinstance(self.date_closed, datetime.datetime):
            date_closed = self.date_closed.isoformat()
        else:
            date_closed = self.date_closed

        reply_limit = self.reply_limit

        reply_offset = self.reply_offset

        reply_has_more = self.reply_has_more

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "code": code,
                "department_id": department_id,
                "summary": summary,
                "priority": priority,
                "status": status,
                "replies": replies,
            }
        )
        if service_id is not UNSET:
            field_dict["service_id"] = service_id
        if date_added is not UNSET:
            field_dict["date_added"] = date_added
        if date_updated is not UNSET:
            field_dict["date_updated"] = date_updated
        if date_closed is not UNSET:
            field_dict["date_closed"] = date_closed
        if reply_limit is not UNSET:
            field_dict["reply_limit"] = reply_limit
        if reply_offset is not UNSET:
            field_dict["reply_offset"] = reply_offset
        if reply_has_more is not UNSET:
            field_dict["reply_has_more"] = reply_has_more

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_support_ticket_response_200_data_replies_item import (
            GetSupportTicketResponse200DataRepliesItem,
        )

        d = dict(src_dict)
        id = d.pop("id")

        code = d.pop("code")

        department_id = d.pop("department_id")

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        priority = GetSupportTicketResponse200DataPriority(d.pop("priority"))

        status = GetSupportTicketResponse200DataStatus(d.pop("status"))

        replies = []
        _replies = d.pop("replies")
        for replies_item_data in _replies:
            replies_item = GetSupportTicketResponse200DataRepliesItem.from_dict(
                replies_item_data
            )

            replies.append(replies_item)

        def _parse_service_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        service_id = _parse_service_id(d.pop("service_id", UNSET))

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

        def _parse_date_closed(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_closed_type_0 = datetime.datetime.fromisoformat(data)

                return date_closed_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_closed = _parse_date_closed(d.pop("date_closed", UNSET))

        reply_limit = d.pop("reply_limit", UNSET)

        reply_offset = d.pop("reply_offset", UNSET)

        reply_has_more = d.pop("reply_has_more", UNSET)

        get_support_ticket_response_200_data = cls(
            id=id,
            code=code,
            department_id=department_id,
            summary=summary,
            priority=priority,
            status=status,
            replies=replies,
            service_id=service_id,
            date_added=date_added,
            date_updated=date_updated,
            date_closed=date_closed,
            reply_limit=reply_limit,
            reply_offset=reply_offset,
            reply_has_more=reply_has_more,
        )

        return get_support_ticket_response_200_data
