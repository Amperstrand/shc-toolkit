from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="EmailDetail")


@_attrs_define
class EmailDetail:
    """Customer-safe email / notice detail with full body.

    Attributes:
        id (int):  Example: 501.
        subject (None | str):  Example: Invoice #123.
        from_address (None | str):  Example: billing@example.com.
        from_name (None | str):  Example: Billing.
        to_address (None | str):  Example: client@example.com.
        cc_address (list[str]):
        sent (bool):  Example: True.
        error (None | str):
        date_sent (datetime.datetime | None):
        body_text (None | str):
        body_html (None | str):
    """

    id: int
    subject: None | str
    from_address: None | str
    from_name: None | str
    to_address: None | str
    cc_address: list[str]
    sent: bool
    error: None | str
    date_sent: datetime.datetime | None
    body_text: None | str
    body_html: None | str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        subject: None | str
        subject = self.subject

        from_address: None | str
        from_address = self.from_address

        from_name: None | str
        from_name = self.from_name

        to_address: None | str
        to_address = self.to_address

        cc_address = self.cc_address

        sent = self.sent

        error: None | str
        error = self.error

        date_sent: None | str
        if isinstance(self.date_sent, datetime.datetime):
            date_sent = self.date_sent.isoformat()
        else:
            date_sent = self.date_sent

        body_text: None | str
        body_text = self.body_text

        body_html: None | str
        body_html = self.body_html

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "subject": subject,
                "from_address": from_address,
                "from_name": from_name,
                "to_address": to_address,
                "cc_address": cc_address,
                "sent": sent,
                "error": error,
                "date_sent": date_sent,
                "body_text": body_text,
                "body_html": body_html,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_subject(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        subject = _parse_subject(d.pop("subject"))

        def _parse_from_address(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        from_address = _parse_from_address(d.pop("from_address"))

        def _parse_from_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        from_name = _parse_from_name(d.pop("from_name"))

        def _parse_to_address(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        to_address = _parse_to_address(d.pop("to_address"))

        cc_address = cast(list[str], d.pop("cc_address"))

        sent = d.pop("sent")

        def _parse_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error = _parse_error(d.pop("error"))

        def _parse_date_sent(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_sent_type_0 = datetime.datetime.fromisoformat(data)

                return date_sent_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_sent = _parse_date_sent(d.pop("date_sent"))

        def _parse_body_text(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        body_text = _parse_body_text(d.pop("body_text"))

        def _parse_body_html(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        body_html = _parse_body_html(d.pop("body_html"))

        email_detail = cls(
            id=id,
            subject=subject,
            from_address=from_address,
            from_name=from_name,
            to_address=to_address,
            cc_address=cc_address,
            sent=sent,
            error=error,
            date_sent=date_sent,
            body_text=body_text,
            body_html=body_html,
        )

        return email_detail
