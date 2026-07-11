from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.invoice_status import InvoiceStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.applied_payment import AppliedPayment
    from ..models.invoice_line_item_list import InvoiceLineItemList


T = TypeVar("T", bound="AccountInvoiceDetail")


@_attrs_define
class AccountInvoiceDetail:
    """Customer-safe single invoice with line items and optional applied payments.

    Attributes:
        id (int):  Example: 123.
        id_code (str):  Example: 123.
        invoice_status (InvoiceStatus): Blesta invoice lifecycle state. `past_due` indicates an open invoice whose due
            date has passed; clients that previously treated it as `open` can continue to do so but the API surfaces the
            distinction. Example: open.
        subtotal (str):  Example: 10.00.
        total (str):  Example: 11.99.
        paid (str):  Example: 0.00.
        previous_due (str):  Example: 0.00.
        currency (str):  Example: USD.
        date_billed (datetime.datetime | None):
        date_due (datetime.datetime | None):
        date_closed (datetime.datetime | None):
        note (None | str):
        line_items (InvoiceLineItemList):
        applied_payments (list[AppliedPayment] | Unset): Present only when the inv_display_payments company setting is
            enabled.
    """

    id: int
    id_code: str
    invoice_status: InvoiceStatus
    subtotal: str
    total: str
    paid: str
    previous_due: str
    currency: str
    date_billed: datetime.datetime | None
    date_due: datetime.datetime | None
    date_closed: datetime.datetime | None
    note: None | str
    line_items: InvoiceLineItemList
    applied_payments: list[AppliedPayment] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        id_code = self.id_code

        invoice_status = self.invoice_status.value

        subtotal = self.subtotal

        total = self.total

        paid = self.paid

        previous_due = self.previous_due

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

        applied_payments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.applied_payments, Unset):
            applied_payments = []
            for applied_payments_item_data in self.applied_payments:
                applied_payments_item = applied_payments_item_data.to_dict()
                applied_payments.append(applied_payments_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "id_code": id_code,
                "invoice_status": invoice_status,
                "subtotal": subtotal,
                "total": total,
                "paid": paid,
                "previous_due": previous_due,
                "currency": currency,
                "date_billed": date_billed,
                "date_due": date_due,
                "date_closed": date_closed,
                "note": note,
                "line_items": line_items,
            }
        )
        if applied_payments is not UNSET:
            field_dict["applied_payments"] = applied_payments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.applied_payment import AppliedPayment
        from ..models.invoice_line_item_list import InvoiceLineItemList

        d = dict(src_dict)
        id = d.pop("id")

        id_code = d.pop("id_code")

        invoice_status = InvoiceStatus(d.pop("invoice_status"))

        subtotal = d.pop("subtotal")

        total = d.pop("total")

        paid = d.pop("paid")

        previous_due = d.pop("previous_due")

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

        line_items = InvoiceLineItemList.from_dict(d.pop("line_items"))

        _applied_payments = d.pop("applied_payments", UNSET)
        applied_payments: list[AppliedPayment] | Unset = UNSET
        if _applied_payments is not UNSET:
            applied_payments = []
            for applied_payments_item_data in _applied_payments:
                applied_payments_item = AppliedPayment.from_dict(
                    applied_payments_item_data
                )

                applied_payments.append(applied_payments_item)

        account_invoice_detail = cls(
            id=id,
            id_code=id_code,
            invoice_status=invoice_status,
            subtotal=subtotal,
            total=total,
            paid=paid,
            previous_due=previous_due,
            currency=currency,
            date_billed=date_billed,
            date_due=date_due,
            date_closed=date_closed,
            note=note,
            line_items=line_items,
            applied_payments=applied_payments,
        )

        return account_invoice_detail
