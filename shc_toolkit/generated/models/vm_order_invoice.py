from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.invoice_status import InvoiceStatus

T = TypeVar("T", bound="VmOrderInvoice")


@_attrs_define
class VmOrderInvoice:
    """
    Attributes:
        invoice_id (int):  Example: 1550.
        invoice_status (InvoiceStatus | None):  Example: open.
        currency (str):  Example: USD.
        total (str):  Example: 11.99.
        paid (str):  Example: 0.00.
        balance_due (str):  Example: 11.99.
        date_due (datetime.datetime | None):  Example: 2026-04-24T00:00:00+00:00.
    """

    invoice_id: int
    invoice_status: InvoiceStatus | None
    currency: str
    total: str
    paid: str
    balance_due: str
    date_due: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        invoice_id = self.invoice_id

        invoice_status: None | str
        if isinstance(self.invoice_status, InvoiceStatus):
            invoice_status = self.invoice_status.value
        else:
            invoice_status = self.invoice_status

        currency = self.currency

        total = self.total

        paid = self.paid

        balance_due = self.balance_due

        date_due: None | str
        if isinstance(self.date_due, datetime.datetime):
            date_due = self.date_due.isoformat()
        else:
            date_due = self.date_due

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "invoice_id": invoice_id,
                "invoice_status": invoice_status,
                "currency": currency,
                "total": total,
                "paid": paid,
                "balance_due": balance_due,
                "date_due": date_due,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        invoice_id = d.pop("invoice_id")

        def _parse_invoice_status(data: object) -> InvoiceStatus | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                invoice_status_type_0 = InvoiceStatus(data)

                return invoice_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InvoiceStatus | None, data)

        invoice_status = _parse_invoice_status(d.pop("invoice_status"))

        currency = d.pop("currency")

        total = d.pop("total")

        paid = d.pop("paid")

        balance_due = d.pop("balance_due")

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

        vm_order_invoice = cls(
            invoice_id=invoice_id,
            invoice_status=invoice_status,
            currency=currency,
            total=total,
            paid=paid,
            balance_due=balance_due,
            date_due=date_due,
        )

        vm_order_invoice.additional_properties = d
        return vm_order_invoice

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
