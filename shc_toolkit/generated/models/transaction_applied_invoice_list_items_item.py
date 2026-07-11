from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="TransactionAppliedInvoiceListItemsItem")


@_attrs_define
class TransactionAppliedInvoiceListItemsItem:
    """
    Attributes:
        invoice_id (int):  Example: 123.
        invoice_id_code (str):  Example: 123.
        amount (str):  Example: 11.99.
        date (datetime.datetime | None):
    """

    invoice_id: int
    invoice_id_code: str
    amount: str
    date: datetime.datetime | None

    def to_dict(self) -> dict[str, Any]:
        invoice_id = self.invoice_id

        invoice_id_code = self.invoice_id_code

        amount = self.amount

        date: None | str
        if isinstance(self.date, datetime.datetime):
            date = self.date.isoformat()
        else:
            date = self.date

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "invoice_id": invoice_id,
                "invoice_id_code": invoice_id_code,
                "amount": amount,
                "date": date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        invoice_id = d.pop("invoice_id")

        invoice_id_code = d.pop("invoice_id_code")

        amount = d.pop("amount")

        def _parse_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_type_0 = datetime.datetime.fromisoformat(data)

                return date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date = _parse_date(d.pop("date"))

        transaction_applied_invoice_list_items_item = cls(
            invoice_id=invoice_id,
            invoice_id_code=invoice_id_code,
            amount=amount,
            date=date,
        )

        return transaction_applied_invoice_list_items_item
