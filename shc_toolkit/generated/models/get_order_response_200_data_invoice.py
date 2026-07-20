from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="GetOrderResponse200DataInvoice")


@_attrs_define
class GetOrderResponse200DataInvoice:
    """
    Attributes:
        invoice_id (int):
        invoice_id_code (str):
        currency (str):
        total (str): Fixed two-decimal money string.
        paid (str): Fixed two-decimal money string.
        balance_due (str): Fixed two-decimal money string.
        date_closed (None | str): Raw Blesta invoice close timestamp.
    """

    invoice_id: int
    invoice_id_code: str
    currency: str
    total: str
    paid: str
    balance_due: str
    date_closed: None | str

    def to_dict(self) -> dict[str, Any]:
        invoice_id = self.invoice_id

        invoice_id_code = self.invoice_id_code

        currency = self.currency

        total = self.total

        paid = self.paid

        balance_due = self.balance_due

        date_closed: None | str
        date_closed = self.date_closed

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "invoice_id": invoice_id,
                "invoice_id_code": invoice_id_code,
                "currency": currency,
                "total": total,
                "paid": paid,
                "balance_due": balance_due,
                "date_closed": date_closed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        invoice_id = d.pop("invoice_id")

        invoice_id_code = d.pop("invoice_id_code")

        currency = d.pop("currency")

        total = d.pop("total")

        paid = d.pop("paid")

        balance_due = d.pop("balance_due")

        def _parse_date_closed(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        date_closed = _parse_date_closed(d.pop("date_closed"))

        get_order_response_200_data_invoice = cls(
            invoice_id=invoice_id,
            invoice_id_code=invoice_id_code,
            currency=currency,
            total=total,
            paid=paid,
            balance_due=balance_due,
            date_closed=date_closed,
        )

        return get_order_response_200_data_invoice
