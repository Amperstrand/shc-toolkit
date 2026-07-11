from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NextCheckout")


@_attrs_define
class NextCheckout:
    """Checkout pointer for a payment-gated, queued change (package upgrade).

    Attributes:
        checkout_url (str):  Example: /user-api/v2/payment/9012/checkout.
        note (str | Unset):  Example: The package change is queued; it is applied automatically once the prorated
            invoice is paid. A disk size increase takes effect after you reboot the VM..
    """

    checkout_url: str
    note: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checkout_url = self.checkout_url

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "checkout_url": checkout_url,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checkout_url = d.pop("checkout_url")

        note = d.pop("note", UNSET)

        next_checkout = cls(
            checkout_url=checkout_url,
            note=note,
        )

        next_checkout.additional_properties = d
        return next_checkout

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
