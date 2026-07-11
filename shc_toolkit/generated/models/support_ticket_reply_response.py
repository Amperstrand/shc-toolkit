from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.support_ticket_reply_response_reply import (
        SupportTicketReplyResponseReply,
    )


T = TypeVar("T", bound="SupportTicketReplyResponse")


@_attrs_define
class SupportTicketReplyResponse:
    """
    Attributes:
        ticket_id (int):  Example: 501.
        status (str):  Example: open.
        reply (SupportTicketReplyResponseReply):
    """

    ticket_id: int
    status: str
    reply: SupportTicketReplyResponseReply
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ticket_id = self.ticket_id

        status = self.status

        reply = self.reply.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ticket_id": ticket_id,
                "status": status,
                "reply": reply,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.support_ticket_reply_response_reply import (
            SupportTicketReplyResponseReply,
        )

        d = dict(src_dict)
        ticket_id = d.pop("ticket_id")

        status = d.pop("status")

        reply = SupportTicketReplyResponseReply.from_dict(d.pop("reply"))

        support_ticket_reply_response = cls(
            ticket_id=ticket_id,
            status=status,
            reply=reply,
        )

        support_ticket_reply_response.additional_properties = d
        return support_ticket_reply_response

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
