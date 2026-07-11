from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.invoice_status import InvoiceStatus

if TYPE_CHECKING:
    from ..models.invoice_line_list import InvoiceLineList


T = TypeVar("T", bound="InvoiceDetail")


@_attrs_define
class InvoiceDetail:
    """
    Example:
        {'id': 123, 'invoice_status': 'open', 'subtotal': '11.99', 'total': '11.99', 'paid': '0.00', 'currency': 'USD',
            'date_billed': '2026-02-01T07:57:55+00:00', 'date_due': '2026-02-08T07:57:55+00:00', 'date_closed': None,
            'note': None, 'line_items': {'items': [{'description': 'NVMe VPS - Standard', 'qty': 1, 'amount': '11.99'}],
            'pagination': {'total': 1, 'limit': 100, 'offset': 0, 'has_more': False}}}

    Attributes:
        id (int):  Example: 123.
        invoice_status (InvoiceStatus): Blesta invoice lifecycle state. `past_due` indicates an open invoice whose due
            date has passed; clients that previously treated it as `open` can continue to do so but the API surfaces the
            distinction. Example: open.
        subtotal (str):  Example: 11.99.
        total (str):  Example: 11.99.
        paid (str):  Example: 0.00.
        currency (str):  Example: USD.
        date_billed (datetime.datetime | None):  Example: 2026-02-01T07:57:55+00:00.
        date_due (datetime.datetime | None):  Example: 2026-02-08T07:57:55+00:00.
        date_closed (datetime.datetime | None):  Example: 2026-02-08T08:30:00+00:00.
        note (None | str):
        line_items (InvoiceLineList): Canonical paginated list of invoice line items.
    """

    id: int
    invoice_status: InvoiceStatus
    subtotal: str
    total: str
    paid: str
    currency: str
    date_billed: datetime.datetime | None
    date_due: datetime.datetime | None
    date_closed: datetime.datetime | None
    note: None | str
    line_items: InvoiceLineList
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        invoice_status = self.invoice_status.value

        subtotal = self.subtotal

        total = self.total

        paid = self.paid

        currency = self.currency

        date_billed: None | str
        if isinstance(self.date_billed, datetime.datetime):
            date_billed = self.date_billed.isoformat()
        else:
            date_billed = self.date_billed

        date_due: None | str
        if isinstance(self.date_due, datetime.datetime):
            date_due = self.date_due.isoformat()
        else:
            date_due = self.date_due

        date_closed: None | str
        if isinstance(self.date_closed, datetime.datetime):
            date_closed = self.date_closed.isoformat()
        else:
            date_closed = self.date_closed

        note: None | str
        note = self.note

        line_items = self.line_items.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "invoice_status": invoice_status,
                "subtotal": subtotal,
                "total": total,
                "paid": paid,
                "currency": currency,
                "date_billed": date_billed,
                "date_due": date_due,
                "date_closed": date_closed,
                "note": note,
                "line_items": line_items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invoice_line_list import InvoiceLineList

        d = dict(src_dict)
        id = d.pop("id")

        invoice_status = InvoiceStatus(d.pop("invoice_status"))

        subtotal = d.pop("subtotal")

        total = d.pop("total")

        paid = d.pop("paid")

        currency = d.pop("currency")

        def _parse_date_billed(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_billed_type_0 = datetime.datetime.fromisoformat(data)

                return date_billed_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_billed = _parse_date_billed(d.pop("date_billed"))

        def _parse_date_due(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_due_type_0 = datetime.datetime.fromisoformat(data)

                return date_due_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_due = _parse_date_due(d.pop("date_due"))

        def _parse_date_closed(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_closed_type_0 = datetime.datetime.fromisoformat(data)

                return date_closed_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_closed = _parse_date_closed(d.pop("date_closed"))

        def _parse_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        line_items = InvoiceLineList.from_dict(d.pop("line_items"))

        invoice_detail = cls(
            id=id,
            invoice_status=invoice_status,
            subtotal=subtotal,
            total=total,
            paid=paid,
            currency=currency,
            date_billed=date_billed,
            date_due=date_due,
            date_closed=date_closed,
            note=note,
            line_items=line_items,
        )

        invoice_detail.additional_properties = d
        return invoice_detail

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
