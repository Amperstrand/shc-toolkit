from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="GetVirtualMachineTermOptionsResponse200DataItemsItem")


@_attrs_define
class GetVirtualMachineTermOptionsResponse200DataItemsItem:
    """
    Attributes:
        pricing_id (int):
        term (int):
        period (str):
        price (str): Fixed two-decimal money string.
        price_renews (None | str): Fixed two-decimal renewal money string, or null when no renewal override exists.
        currency (str):
        is_current (bool): Whether this term is the service's current pricing.
    """

    pricing_id: int
    term: int
    period: str
    price: str
    price_renews: None | str
    currency: str
    is_current: bool

    def to_dict(self) -> dict[str, Any]:
        pricing_id = self.pricing_id

        term = self.term

        period = self.period

        price = self.price

        price_renews: None | str
        price_renews = self.price_renews

        currency = self.currency

        is_current = self.is_current

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "pricing_id": pricing_id,
                "term": term,
                "period": period,
                "price": price,
                "price_renews": price_renews,
                "currency": currency,
                "is_current": is_current,
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

        def _parse_price_renews(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        price_renews = _parse_price_renews(d.pop("price_renews"))

        currency = d.pop("currency")

        is_current = d.pop("is_current")

        get_virtual_machine_term_options_response_200_data_items_item = cls(
            pricing_id=pricing_id,
            term=term,
            period=period,
            price=price,
            price_renews=price_renews,
            currency=currency,
            is_current=is_current,
        )

        return get_virtual_machine_term_options_response_200_data_items_item
