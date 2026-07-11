from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_account_balance_response_200_data_balances_item import (
        GetAccountBalanceResponse200DataBalancesItem,
    )
    from ..models.get_account_balance_response_200_data_credit_item import (
        GetAccountBalanceResponse200DataCreditItem,
    )
    from ..models.get_account_balance_response_200_data_due_item import (
        GetAccountBalanceResponse200DataDueItem,
    )


T = TypeVar("T", bound="GetAccountBalanceResponse200Data")


@_attrs_define
class GetAccountBalanceResponse200Data:
    """
    Attributes:
        due (list[GetAccountBalanceResponse200DataDueItem]):
        credit (list[GetAccountBalanceResponse200DataCreditItem]):
        balances (list[GetAccountBalanceResponse200DataBalancesItem] | Unset): v2.4.0 alias (additive): identical to
            'credit' — the name /billing/balance uses.
    """

    due: list[GetAccountBalanceResponse200DataDueItem]
    credit: list[GetAccountBalanceResponse200DataCreditItem]
    balances: list[GetAccountBalanceResponse200DataBalancesItem] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        due = []
        for due_item_data in self.due:
            due_item = due_item_data.to_dict()
            due.append(due_item)

        credit = []
        for credit_item_data in self.credit:
            credit_item = credit_item_data.to_dict()
            credit.append(credit_item)

        balances: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.balances, Unset):
            balances = []
            for balances_item_data in self.balances:
                balances_item = balances_item_data.to_dict()
                balances.append(balances_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "due": due,
                "credit": credit,
            }
        )
        if balances is not UNSET:
            field_dict["balances"] = balances

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_account_balance_response_200_data_balances_item import (
            GetAccountBalanceResponse200DataBalancesItem,
        )
        from ..models.get_account_balance_response_200_data_credit_item import (
            GetAccountBalanceResponse200DataCreditItem,
        )
        from ..models.get_account_balance_response_200_data_due_item import (
            GetAccountBalanceResponse200DataDueItem,
        )

        d = dict(src_dict)
        due = []
        _due = d.pop("due")
        for due_item_data in _due:
            due_item = GetAccountBalanceResponse200DataDueItem.from_dict(due_item_data)

            due.append(due_item)

        credit = []
        _credit = d.pop("credit")
        for credit_item_data in _credit:
            credit_item = GetAccountBalanceResponse200DataCreditItem.from_dict(
                credit_item_data
            )

            credit.append(credit_item)

        _balances = d.pop("balances", UNSET)
        balances: list[GetAccountBalanceResponse200DataBalancesItem] | Unset = UNSET
        if _balances is not UNSET:
            balances = []
            for balances_item_data in _balances:
                balances_item = GetAccountBalanceResponse200DataBalancesItem.from_dict(
                    balances_item_data
                )

                balances.append(balances_item)

        get_account_balance_response_200_data = cls(
            due=due,
            credit=credit,
            balances=balances,
        )

        return get_account_balance_response_200_data
