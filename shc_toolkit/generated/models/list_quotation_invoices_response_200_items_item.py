from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.invoice_status import InvoiceStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListQuotationInvoicesResponse200ItemsItem")


@_attrs_define
class ListQuotationInvoicesResponse200ItemsItem:
    """
    Attributes:
        id (int):  Example: 9100.
        invoice_status (InvoiceStatus): Blesta invoice lifecycle state. `past_due` indicates an open invoice whose due
            date has passed; clients that previously treated it as `open` can continue to do so but the API surfaces the
            distinction. Example: open.
        total (str):  Example: 120.00.
        paid (str):  Example: 0.00.
        currency (str):  Example: USD.
        date_billed (datetime.datetime | None | Unset):
        date_due (datetime.datetime | None | Unset):
        date_closed (datetime.datetime | None | Unset):
    """

    id: int
    invoice_status: InvoiceStatus
    total: str
    paid: str
    currency: str
    date_billed: datetime.datetime | None | Unset = UNSET
    date_due: datetime.datetime | None | Unset = UNSET
    date_closed: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        invoice_status = self.invoice_status.value

        total = self.total

        paid = self.paid

        currency = self.currency

        date_billed: None | str | Unset
        if isinstance(self.date_billed, Unset):
            date_billed = UNSET
        elif isinstance(self.date_billed, datetime.datetime):
            date_billed = self.date_billed.isoformat()
        else:
            date_billed = self.date_billed

        date_due: None | str | Unset
        if isinstance(self.date_due, Unset):
            date_due = UNSET
        elif isinstance(self.date_due, datetime.datetime):
            date_due = self.date_due.isoformat()
        else:
            date_due = self.date_due

        date_closed: None | str | Unset
        if isinstance(self.date_closed, Unset):
            date_closed = UNSET
        elif isinstance(self.date_closed, datetime.datetime):
            date_closed = self.date_closed.isoformat()
        else:
            date_closed = self.date_closed

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "invoice_status": invoice_status,
                "total": total,
                "paid": paid,
                "currency": currency,
            }
        )
        if date_billed is not UNSET:
            field_dict["date_billed"] = date_billed
        if date_due is not UNSET:
            field_dict["date_due"] = date_due
        if date_closed is not UNSET:
            field_dict["date_closed"] = date_closed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        invoice_status = InvoiceStatus(d.pop("invoice_status"))

        total = d.pop("total")

        paid = d.pop("paid")

        currency = d.pop("currency")

        def _parse_date_billed(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_billed_type_0 = datetime.datetime.fromisoformat(data)

                return date_billed_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_billed = _parse_date_billed(d.pop("date_billed", UNSET))

        def _parse_date_due(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_due_type_0 = datetime.datetime.fromisoformat(data)

                return date_due_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_due = _parse_date_due(d.pop("date_due", UNSET))

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

        list_quotation_invoices_response_200_items_item = cls(
            id=id,
            invoice_status=invoice_status,
            total=total,
            paid=paid,
            currency=currency,
            date_billed=date_billed,
            date_due=date_due,
            date_closed=date_closed,
        )

        return list_quotation_invoices_response_200_items_item
