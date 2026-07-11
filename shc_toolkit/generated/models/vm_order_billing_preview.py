from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmOrderBillingPreview")


@_attrs_define
class VmOrderBillingPreview:
    """
    Attributes:
        pricing_id (int):  Example: 12.
        term (int):  Example: 1.
        period (str):  Example: month.
        price (str):  Example: 11.99.
        renew (None | str):  Example: 11.99.
        setup_fee (str):  Example: 0.00.
        currency (str):  Example: USD.
        initial_due (str):  Example: 11.99.
        renewal_amount (str):  Example: 11.99.
    """

    pricing_id: int
    term: int
    period: str
    price: str
    renew: None | str
    setup_fee: str
    currency: str
    initial_due: str
    renewal_amount: str
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

        initial_due = self.initial_due

        renewal_amount = self.renewal_amount

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
                "initial_due": initial_due,
                "renewal_amount": renewal_amount,
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

        initial_due = d.pop("initial_due")

        renewal_amount = d.pop("renewal_amount")

        vm_order_billing_preview = cls(
            pricing_id=pricing_id,
            term=term,
            period=period,
            price=price,
            renew=renew,
            setup_fee=setup_fee,
            currency=currency,
            initial_due=initial_due,
            renewal_amount=renewal_amount,
        )

        vm_order_billing_preview.additional_properties = d
        return vm_order_billing_preview

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
