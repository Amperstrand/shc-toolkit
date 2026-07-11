from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="VmOrderNext")


@_attrs_define
class VmOrderNext:
    """
    Attributes:
        payment_required (bool):  Example: True.
        checkout_url (None | str): Relative checkout hand-off for the invoice created by `POST /ordering/submit`. Null
            when the invoice balance is already zero. Example: /payment/1550/checkout.
        manual_review (bool):
        provisioning (str):  Example: Provisioning begins after the order is accepted and the invoice is paid..
    """

    payment_required: bool
    checkout_url: None | str
    manual_review: bool
    provisioning: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payment_required = self.payment_required

        checkout_url: None | str
        checkout_url = self.checkout_url

        manual_review = self.manual_review

        provisioning = self.provisioning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payment_required": payment_required,
                "checkout_url": checkout_url,
                "manual_review": manual_review,
                "provisioning": provisioning,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        payment_required = d.pop("payment_required")

        def _parse_checkout_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        checkout_url = _parse_checkout_url(d.pop("checkout_url"))

        manual_review = d.pop("manual_review")

        provisioning = d.pop("provisioning")

        vm_order_next = cls(
            payment_required=payment_required,
            checkout_url=checkout_url,
            manual_review=manual_review,
            provisioning=provisioning,
        )

        vm_order_next.additional_properties = d
        return vm_order_next

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
