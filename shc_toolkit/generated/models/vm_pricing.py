from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmPricing")


@_attrs_define
class VmPricing:
    """Current billing cadence and pricing for one owned service.

    Example:
        {'term': 1, 'period': 'month', 'price': '11.99', 'renew': '11.99', 'currency': 'USD'}

    Attributes:
        term (int): Billing term count for the active pricing row. Example: 1.
        period (None | str): Billing period unit such as `month` or `year`. Example: month.
        price (str): Current billed amount for the active cadence. Example: 11.99.
        renew (str): Renewal amount for the active cadence. Example: 11.99.
        currency (str): ISO-style currency code used for pricing fields. Example: USD.
    """

    term: int
    period: None | str
    price: str
    renew: str
    currency: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        term = self.term

        period: None | str
        period = self.period

        price = self.price

        renew = self.renew

        currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "term": term,
                "period": period,
                "price": price,
                "renew": renew,
                "currency": currency,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        term = d.pop("term")

        def _parse_period(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        period = _parse_period(d.pop("period"))

        price = d.pop("price")

        renew = d.pop("renew")

        currency = d.pop("currency")

        vm_pricing = cls(
            term=term,
            period=period,
            price=price,
            renew=renew,
            currency=currency,
        )

        vm_pricing.additional_properties = d
        return vm_pricing

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
