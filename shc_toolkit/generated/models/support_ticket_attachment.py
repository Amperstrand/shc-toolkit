from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SupportTicketAttachment")


@_attrs_define
class SupportTicketAttachment:
    """A base64-encoded file to attach to a ticket or reply.

    Attributes:
        name (str): File name (no path separators). Example: screenshot.png.
        content_base64 (str): Standard base64-encoded file content. Example: iVBORw0KGgoAAAANSUhEUgAA....
        content_type (None | str | Unset): MIME type. Defaults to application/octet-stream. Example: image/png.
    """

    name: str
    content_base64: str
    content_type: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        content_base64 = self.content_base64

        content_type: None | str | Unset
        if isinstance(self.content_type, Unset):
            content_type = UNSET
        else:
            content_type = self.content_type

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "content_base64": content_base64,
            }
        )
        if content_type is not UNSET:
            field_dict["content_type"] = content_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        content_base64 = d.pop("content_base64")

        def _parse_content_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        content_type = _parse_content_type(d.pop("content_type", UNSET))

        support_ticket_attachment = cls(
            name=name,
            content_base64=content_base64,
            content_type=content_type,
        )

        return support_ticket_attachment
