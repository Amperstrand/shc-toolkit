from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.support_ticket_attachment import SupportTicketAttachment
    from ..models.support_ticket_custom_fields import SupportTicketCustomFields


T = TypeVar("T", bound="SupportTicketReplyRequest")


@_attrs_define
class SupportTicketReplyRequest:
    """Add a reply to an owned ticket. Replying to a closed/awaiting-reply ticket reopens it.

    Example:
        {'message': 'Still happening after a reboot.'}

    Attributes:
        message (str): Reply body. Example: Still happening after a reboot..
        custom_fields (SupportTicketCustomFields | Unset): Department custom-field values keyed by numeric field id.
            Values are scalar (string/number/boolean). Example: {'12': 'value', '15': True}.
        attachments (list[SupportTicketAttachment] | Unset):
    """

    message: str
    custom_fields: SupportTicketCustomFields | Unset = UNSET
    attachments: list[SupportTicketAttachment] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        custom_fields: dict[str, Any] | Unset = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        attachments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
            }
        )
        if custom_fields is not UNSET:
            field_dict["custom_fields"] = custom_fields
        if attachments is not UNSET:
            field_dict["attachments"] = attachments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.support_ticket_attachment import SupportTicketAttachment
        from ..models.support_ticket_custom_fields import SupportTicketCustomFields

        d = dict(src_dict)
        message = d.pop("message")

        _custom_fields = d.pop("custom_fields", UNSET)
        custom_fields: SupportTicketCustomFields | Unset
        if isinstance(_custom_fields, Unset):
            custom_fields = UNSET
        else:
            custom_fields = SupportTicketCustomFields.from_dict(_custom_fields)

        _attachments = d.pop("attachments", UNSET)
        attachments: list[SupportTicketAttachment] | Unset = UNSET
        if _attachments is not UNSET:
            attachments = []
            for attachments_item_data in _attachments:
                attachments_item = SupportTicketAttachment.from_dict(
                    attachments_item_data
                )

                attachments.append(attachments_item)

        support_ticket_reply_request = cls(
            message=message,
            custom_fields=custom_fields,
            attachments=attachments,
        )

        return support_ticket_reply_request
