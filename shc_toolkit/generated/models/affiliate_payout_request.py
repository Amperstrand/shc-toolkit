from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AffiliatePayoutRequest")


@_attrs_define
class AffiliatePayoutRequest:
    """
    Example:
        {'requested_amount': '0.001', 'requested_currency': 'BTC'}

    Attributes:
        requested_amount (float | str): Amount to withdraw, BTC. Must be > 0, <= available balance, and within min/max
            withdrawal limits. Example: 0.001.
        requested_currency (str | Unset): Optional; must equal the affiliate withdrawal currency (BTC). Example: BTC.
        payment_method_id (int | Unset): Optional payout method id; defaults to the single configured method. Example:
            1.
    """

    requested_amount: float | str
    requested_currency: str | Unset = UNSET
    payment_method_id: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        requested_amount: float | str
        requested_amount = self.requested_amount

        requested_currency = self.requested_currency

        payment_method_id = self.payment_method_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "requested_amount": requested_amount,
            }
        )
        if requested_currency is not UNSET:
            field_dict["requested_currency"] = requested_currency
        if payment_method_id is not UNSET:
            field_dict["payment_method_id"] = payment_method_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_requested_amount(data: object) -> float | str:
            return cast(float | str, data)

        requested_amount = _parse_requested_amount(d.pop("requested_amount"))

        requested_currency = d.pop("requested_currency", UNSET)

        payment_method_id = d.pop("payment_method_id", UNSET)

        affiliate_payout_request = cls(
            requested_amount=requested_amount,
            requested_currency=requested_currency,
            payment_method_id=payment_method_id,
        )

        return affiliate_payout_request
