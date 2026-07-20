from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="GetOrderResponse200DataNext")


@_attrs_define
class GetOrderResponse200DataNext:
    """
    Attributes:
        payment_required (bool):
        checkout_url (None | str): Relative checkout URL when payment is still required.
    """

    payment_required: bool
    checkout_url: None | str

    def to_dict(self) -> dict[str, Any]:
        payment_required = self.payment_required

        checkout_url: None | str
        checkout_url = self.checkout_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "payment_required": payment_required,
                "checkout_url": checkout_url,
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

        get_order_response_200_data_next = cls(
            payment_required=payment_required,
            checkout_url=checkout_url,
        )

        return get_order_response_200_data_next
