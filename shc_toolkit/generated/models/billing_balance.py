from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_balance_credit_item import BillingBalanceCreditItem
    from ..models.billing_currency_balance import BillingCurrencyBalance


T = TypeVar("T", bound="BillingBalance")


@_attrs_define
class BillingBalance:
    """
    Attributes:
        default_currency (str):  Example: USD.
        selected_currency (str):  Example: USD.
        payment_credit_enabled (bool):  Example: True.
        balances (list[BillingCurrencyBalance]):
        credit (list[BillingBalanceCreditItem] | Unset): v2.4.0 alias (additive): per-currency available credit as
            {currency, amount} — the same list /account/balance calls 'credit'.
    """

    default_currency: str
    selected_currency: str
    payment_credit_enabled: bool
    balances: list[BillingCurrencyBalance]
    credit: list[BillingBalanceCreditItem] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        default_currency = self.default_currency

        selected_currency = self.selected_currency

        payment_credit_enabled = self.payment_credit_enabled

        balances = []
        for balances_item_data in self.balances:
            balances_item = balances_item_data.to_dict()
            balances.append(balances_item)

        credit: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.credit, Unset):
            credit = []
            for credit_item_data in self.credit:
                credit_item = credit_item_data.to_dict()
                credit.append(credit_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "default_currency": default_currency,
                "selected_currency": selected_currency,
                "payment_credit_enabled": payment_credit_enabled,
                "balances": balances,
            }
        )
        if credit is not UNSET:
            field_dict["credit"] = credit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_balance_credit_item import BillingBalanceCreditItem
        from ..models.billing_currency_balance import BillingCurrencyBalance

        d = dict(src_dict)
        default_currency = d.pop("default_currency")

        selected_currency = d.pop("selected_currency")

        payment_credit_enabled = d.pop("payment_credit_enabled")

        balances = []
        _balances = d.pop("balances")
        for balances_item_data in _balances:
            balances_item = BillingCurrencyBalance.from_dict(balances_item_data)

            balances.append(balances_item)

        _credit = d.pop("credit", UNSET)
        credit: list[BillingBalanceCreditItem] | Unset = UNSET
        if _credit is not UNSET:
            credit = []
            for credit_item_data in _credit:
                credit_item = BillingBalanceCreditItem.from_dict(credit_item_data)

                credit.append(credit_item)

        billing_balance = cls(
            default_currency=default_currency,
            selected_currency=selected_currency,
            payment_credit_enabled=payment_credit_enabled,
            balances=balances,
            credit=credit,
        )

        return billing_balance
