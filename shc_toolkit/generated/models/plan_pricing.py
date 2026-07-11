from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PlanPricing")


@_attrs_define
class PlanPricing:
    """One pricing row available for a package, typically representing a billing cadence.

    Example:
        {'pricing_id': 12, 'term': 1, 'period': 'month', 'price': '11.99', 'renew': '11.99', 'setup_fee': '0.00',
            'currency': 'USD'}

    Attributes:
        pricing_id (int): Blesta pricing row identifier for this specific billing option. Example: 12.
        term (int): Billing term count for this pricing row. Example: 1.
        period (str): Billing period unit such as `month` or `year`. Example: month.
        price (str): Initial billed amount for this pricing row. Example: 11.99.
        renew (None | str): Renewal amount for this pricing row, if distinct from `price`. Example: 11.99.
        setup_fee (str): One-time setup charge associated with this pricing row. Example: 0.00.
        currency (str): ISO-style currency code used for pricing fields. Example: USD.
    """

    pricing_id: int
    term: int
    period: str
    price: str
    renew: None | str
    setup_fee: str
    currency: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pricing_id = self.pricing_id

        term = self.term

        period = self.period

        price = self.price

        renew: None | str
        renew = self.renew

        setup_fee = self.setup_fee

        currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pricing_id": pricing_id,
                "term": term,
                "period": period,
                "price": price,
                "renew": renew,
                "setup_fee": setup_fee,
                "currency": currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pricing_id = d.pop("pricing_id")

        term = d.pop("term")

        period = d.pop("period")

        price = d.pop("price")

        def _parse_renew(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        renew = _parse_renew(d.pop("renew"))

        setup_fee = d.pop("setup_fee")

        currency = d.pop("currency")

        plan_pricing = cls(
            pricing_id=pricing_id,
            term=term,
            period=period,
            price=price,
            renew=renew,
            setup_fee=setup_fee,
            currency=currency,
        )

        plan_pricing.additional_properties = d
        return plan_pricing

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
