from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="GetAccountBalanceResponse200DataCreditItem")


@_attrs_define
class GetAccountBalanceResponse200DataCreditItem:
    """
    Attributes:
        currency (str):  Example: USD.
        amount (str):  Example: 25.00.
    """

    currency: str
    amount: str

    def to_dict(self) -> dict[str, Any]:
        currency = self.currency

        amount = self.amount

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "currency": currency,
                "amount": amount,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        currency = d.pop("currency")

        amount = d.pop("amount")

        get_account_balance_response_200_data_credit_item = cls(
            currency=currency,
            amount=amount,
        )

        return get_account_balance_response_200_data_credit_item
