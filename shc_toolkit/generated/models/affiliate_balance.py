from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AffiliateBalance")


@_attrs_define
class AffiliateBalance:
    """
    Attributes:
        currency (str):  Example: BTC.
        available (str): Available to withdraw now, BTC (8 dp) = total_available - total_withdrawn, floored at 0.
            Example: 0.00000000.
        total_available (str): Lifetime matured commission, BTC (8 dp). Example: 0.00000000.
        total_withdrawn (str): Lifetime withdrawn, BTC (8 dp). Example: 0.00000000.
    """

    currency: str
    available: str
    total_available: str
    total_withdrawn: str

    def to_dict(self) -> dict[str, Any]:
        currency = self.currency

        available = self.available

        total_available = self.total_available

        total_withdrawn = self.total_withdrawn

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "currency": currency,
                "available": available,
                "total_available": total_available,
                "total_withdrawn": total_withdrawn,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        currency = d.pop("currency")

        available = d.pop("available")

        total_available = d.pop("total_available")

        total_withdrawn = d.pop("total_withdrawn")

        affiliate_balance = cls(
            currency=currency,
            available=available,
            total_available=total_available,
            total_withdrawn=total_withdrawn,
        )

        return affiliate_balance
