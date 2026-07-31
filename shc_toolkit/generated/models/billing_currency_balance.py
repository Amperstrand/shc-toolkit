from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="BillingCurrencyBalance")


@_attrs_define
class BillingCurrencyBalance:
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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
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
