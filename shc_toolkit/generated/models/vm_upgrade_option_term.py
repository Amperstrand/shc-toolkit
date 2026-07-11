from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmUpgradeOptionTerm")


@_attrs_define
class VmUpgradeOptionTerm:
    """One client-orderable term for an upgradable plan. pricing_ref is the raw package_pricing id to pass to
    preview/PATCH.

        Attributes:
            pricing_ref (str): Raw package_pricing.id. Example: 57.
            term (int):  Example: 1.
            period (str):  Example: month.
            recurring_amount (str): Recurring price (base plan) at this term. Example: 20.00.
            currency (str):  Example: USD.
            setup_fee (str | Unset): One-time setup fee at this term. Example: 0.00.
    """

    pricing_ref: str
    term: int
    period: str
    recurring_amount: str
    currency: str
    setup_fee: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pricing_ref = self.pricing_ref

        term = self.term

        period = self.period

        recurring_amount = self.recurring_amount

        currency = self.currency

        setup_fee = self.setup_fee

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pricing_ref": pricing_ref,
                "term": term,
                "period": period,
                "recurring_amount": recurring_amount,
                "currency": currency,
            }
        )
        if setup_fee is not UNSET:
            field_dict["setup_fee"] = setup_fee

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pricing_ref = d.pop("pricing_ref")

        term = d.pop("term")

        period = d.pop("period")

        recurring_amount = d.pop("recurring_amount")

        currency = d.pop("currency")

        setup_fee = d.pop("setup_fee", UNSET)

        vm_upgrade_option_term = cls(
            pricing_ref=pricing_ref,
            term=term,
            period=period,
            recurring_amount=recurring_amount,
            currency=currency,
            setup_fee=setup_fee,
        )

        vm_upgrade_option_term.additional_properties = d
        return vm_upgrade_option_term

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
