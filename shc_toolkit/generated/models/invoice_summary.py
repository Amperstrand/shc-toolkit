from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.invoice_status import InvoiceStatus

T = TypeVar("T", bound="InvoiceSummary")


@_attrs_define
class InvoiceSummary:
    """
    Example:
        {'id': 123, 'invoice_status': 'open', 'total': '11.99', 'paid': '0.00', 'currency': 'USD', 'date_billed':
            '2026-02-01T07:57:55+00:00', 'date_due': '2026-02-08T07:57:55+00:00', 'date_closed': None}

    Attributes:
        id (int):  Example: 123.
        invoice_status (InvoiceStatus): Blesta invoice lifecycle state. `past_due` indicates an open invoice whose due
            date has passed; clients that previously treated it as `open` can continue to do so but the API surfaces the
            distinction. Example: open.
        total (str):  Example: 11.99.
        paid (str):  Example: 0.00.
        currency (str):  Example: USD.
        date_billed (datetime.datetime | None):  Example: 2026-02-01T07:57:55+00:00.
        date_due (datetime.datetime | None):  Example: 2026-02-08T07:57:55+00:00.
        date_closed (datetime.datetime | None):  Example: 2026-02-08T08:30:00+00:00.
    """

    id: int
    invoice_status: InvoiceStatus
    total: str
    paid: str
    currency: str
    date_billed: datetime.datetime | None
    date_due: datetime.datetime | None
    date_closed: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        invoice_status = self.invoice_status.value

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "invoice_status": invoice_status,
                "total": total,
                "paid": paid,
                "currency": currency,
                "date_billed": date_billed,
                "date_due": date_due,
                "date_closed": date_closed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        invoice_status = InvoiceStatus(d.pop("invoice_status"))

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

        invoice_summary = cls(
            id=id,
            invoice_status=invoice_status,
            total=total,
            paid=paid,
            currency=currency,
            date_billed=date_billed,
            date_due=date_due,
            date_closed=date_closed,
        )

        invoice_summary.additional_properties = d
        return invoice_summary

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
