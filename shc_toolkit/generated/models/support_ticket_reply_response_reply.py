from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.support_ticket_reply_response_reply_author_type import (
    SupportTicketReplyResponseReplyAuthorType,
)

T = TypeVar("T", bound="SupportTicketReplyResponseReply")


@_attrs_define
class SupportTicketReplyResponseReply:
    """
    Attributes:
        id (int):  Example: 9001.
        author_type (SupportTicketReplyResponseReplyAuthorType):  Example: client.
        author_name (None | str):  Example: Jane Customer.
        details (str):  Example: Still happening after a reboot..
        date_added (None | str): Datetime the reply was recorded. Example: 2026-06-04 14:32:10.
    """

    id: int
    author_type: SupportTicketReplyResponseReplyAuthorType
    author_name: None | str
    details: str
    date_added: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        author_type = self.author_type.value

        author_name: None | str
        author_name = self.author_name

        details = self.details

        date_added: None | str
        date_added = self.date_added

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "author_type": author_type,
                "author_name": author_name,
                "details": details,
                "date_added": date_added,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        author_type = SupportTicketReplyResponseReplyAuthorType(d.pop("author_type"))

        def _parse_author_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        author_name = _parse_author_name(d.pop("author_name"))

        details = d.pop("details")

        def _parse_date_added(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        date_added = _parse_date_added(d.pop("date_added"))

        support_ticket_reply_response_reply = cls(
            id=id,
            author_type=author_type,
            author_name=author_name,
            details=details,
            date_added=date_added,
        )

        support_ticket_reply_response_reply.additional_properties = d
        return support_ticket_reply_response_reply

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
