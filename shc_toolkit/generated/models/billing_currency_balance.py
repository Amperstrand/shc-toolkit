from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="BillingCurrencyBalance")


@_attrs_define
class BillingCurrencyBalance:
    """
    Attributes:
        currency (str):  Example: USD.
        available_credit (str):  Example: 12.50.
        open_invoices_total (str):  Example: 40.00.
        open_invoices_paid (str):  Example: 0.00.
        balance_due (str):  Example: 40.00.
    """

    currency: str
    available_credit: str
    open_invoices_total: str
    open_invoices_paid: str
    balance_due: str

    def to_dict(self) -> dict[str, Any]:
        currency = self.currency

        available_credit = self.available_credit

        open_invoices_total = self.open_invoices_total

        open_invoices_paid = self.open_invoices_paid

        balance_due = self.balance_due

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "currency": currency,
                "available_credit": available_credit,
                "open_invoices_total": open_invoices_total,
                "open_invoices_paid": open_invoices_paid,
                "balance_due": balance_due,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        currency = d.pop("currency")

        available_credit = d.pop("available_credit")

        open_invoices_total = d.pop("open_invoices_total")

        open_invoices_paid = d.pop("open_invoices_paid")

        balance_due = d.pop("balance_due")

        billing_currency_balance = cls(
            currency=currency,
            available_credit=available_credit,
            open_invoices_total=open_invoices_total,
            open_invoices_paid=open_invoices_paid,
            balance_due=balance_due,
        )

        return billing_currency_balance
