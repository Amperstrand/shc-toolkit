from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AffiliateAccountStats")


@_attrs_define
class AffiliateAccountStats:
    """
    Attributes:
        visits (int):  Example: 2.
        sales (int):
        conversion_rate (float): sales / visits as a percentage.
    """

    visits: int
    sales: int
    conversion_rate: float

    def to_dict(self) -> dict[str, Any]:
        visits = self.visits

        sales = self.sales

        conversion_rate = self.conversion_rate

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "visits": visits,
                "sales": sales,
                "conversion_rate": conversion_rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        visits = d.pop("visits")

        sales = d.pop("sales")

        conversion_rate = d.pop("conversion_rate")

        affiliate_account_stats = cls(
            visits=visits,
            sales=sales,
            conversion_rate=conversion_rate,
        )

        return affiliate_account_stats
