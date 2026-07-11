from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.support_ticket_attachment import SupportTicketAttachment
    from ..models.support_ticket_custom_fields import SupportTicketCustomFields


T = TypeVar("T", bound="SupportTicketCreateRequest")


@_attrs_define
class SupportTicketCreateRequest:
    """Create a support ticket. `department_id`, `subject`, and `message` are required.

    Example:
        {'department_id': 1, 'subject': 'Cannot reach my VM over SSH', 'message': 'My VM stopped responding to SSH
            around 14:00 UTC.', 'priority': 'medium'}

    Attributes:
        department_id (int): Target support department (must be visible to this client; see GET /support/departments).
            Example: 1.
        subject (str): Ticket subject/summary. Example: Cannot reach my VM over SSH.
        message (str): Ticket body. Example: My VM stopped responding to SSH around 14:00 UTC..
        priority (str | Unset): Priority key valid for the department. Defaults to the department's default priority.
            Example: medium.
        custom_fields (SupportTicketCustomFields | Unset): Department custom-field values keyed by numeric field id.
            Values are scalar (string/number/boolean). Example: {'12': 'value', '15': True}.
        attachments (list[SupportTicketAttachment] | Unset): Optional base64-encoded attachments (subject to a total-
            size cap).
    """

    department_id: int
    subject: str
    message: str
    priority: str | Unset = UNSET
    custom_fields: SupportTicketCustomFields | Unset = UNSET
    attachments: list[SupportTicketAttachment] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        department_id = self.department_id

        subject = self.subject

        message = self.message

        priority = self.priority

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
                "department_id": department_id,
                "subject": subject,
                "message": message,
            }
        )
        if priority is not UNSET:
            field_dict["priority"] = priority
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
        department_id = d.pop("department_id")

        subject = d.pop("subject")

        message = d.pop("message")

        priority = d.pop("priority", UNSET)

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

        support_ticket_create_request = cls(
            department_id=department_id,
            subject=subject,
            message=message,
            priority=priority,
            custom_fields=custom_fields,
            attachments=attachments,
        )

        return support_ticket_create_request
