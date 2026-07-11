from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="GetAccountBalanceResponse200DataDueItem")


@_attrs_define
class GetAccountBalanceResponse200DataDueItem:
    """
    Attributes:
        currency (str):  Example: USD.
        amount (str):  Example: 120.00.
        past_due (str):  Example: 0.00.
    """

    currency: str
    amount: str
    past_due: str

    def to_dict(self) -> dict[str, Any]:
        currency = self.currency

        amount = self.amount

        past_due = self.past_due

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "currency": currency,
                "amount": amount,
                "past_due": past_due,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        currency = d.pop("currency")

        amount = d.pop("amount")

        past_due = d.pop("past_due")

        get_account_balance_response_200_data_due_item = cls(
            currency=currency,
            amount=amount,
            past_due=past_due,
        )

        return get_account_balance_response_200_data_due_item
