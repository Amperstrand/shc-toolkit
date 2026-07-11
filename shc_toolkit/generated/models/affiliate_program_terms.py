from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.affiliate_program_terms_commission_type import (
    AffiliateProgramTermsCommissionType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AffiliateProgramTerms")


@_attrs_define
class AffiliateProgramTerms:
    """Company-level affiliate program terms (BTC-native).

    Attributes:
        commission_type (AffiliateProgramTermsCommissionType):  Example: percentage.
        commission_amount (str): For percentage, the percent (e.g. "2"); for fixed, a BTC amount. Example: 2.
        withdrawal_currency (str):  Example: BTC.
        min_withdrawal_amount (str): Minimum payout, BTC (8 dp). Example: 0.00100000.
        max_withdrawal_amount (str): Maximum payout, BTC (8 dp). Example: 0.10000000.
        cookie_days (int): Referral attribution cookie window, in days. Example: 90.
        maturity_days (int | Unset): Days before a referral commission matures. Example: 1.
    """

    commission_type: AffiliateProgramTermsCommissionType
    commission_amount: str
    withdrawal_currency: str
    min_withdrawal_amount: str
    max_withdrawal_amount: str
    cookie_days: int
    maturity_days: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        commission_type = self.commission_type.value

        commission_amount = self.commission_amount

        withdrawal_currency = self.withdrawal_currency

        min_withdrawal_amount = self.min_withdrawal_amount

        max_withdrawal_amount = self.max_withdrawal_amount

        cookie_days = self.cookie_days

        maturity_days = self.maturity_days

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "commission_type": commission_type,
                "commission_amount": commission_amount,
                "withdrawal_currency": withdrawal_currency,
                "min_withdrawal_amount": min_withdrawal_amount,
                "max_withdrawal_amount": max_withdrawal_amount,
                "cookie_days": cookie_days,
            }
        )
        if maturity_days is not UNSET:
            field_dict["maturity_days"] = maturity_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        commission_type = AffiliateProgramTermsCommissionType(d.pop("commission_type"))

        commission_amount = d.pop("commission_amount")

        withdrawal_currency = d.pop("withdrawal_currency")

        min_withdrawal_amount = d.pop("min_withdrawal_amount")

        max_withdrawal_amount = d.pop("max_withdrawal_amount")

        cookie_days = d.pop("cookie_days")

        maturity_days = d.pop("maturity_days", UNSET)

        affiliate_program_terms = cls(
            commission_type=commission_type,
            commission_amount=commission_amount,
            withdrawal_currency=withdrawal_currency,
            min_withdrawal_amount=min_withdrawal_amount,
            max_withdrawal_amount=max_withdrawal_amount,
            cookie_days=cookie_days,
            maturity_days=maturity_days,
        )

        return affiliate_program_terms
