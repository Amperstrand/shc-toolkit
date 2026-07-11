from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.affiliate_payout_status import AffiliatePayoutStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AffiliatePayout")


@_attrs_define
class AffiliatePayout:
    """
    Attributes:
        id (int):  Example: 5.
        status (AffiliatePayoutStatus):  Example: pending.
        requested_amount (str): BTC (8 dp). Example: 0.00100000.
        requested_currency (str):  Example: BTC.
        date_requested (datetime.datetime | None):
        paid_amount (None | str | Unset): BTC (8 dp), or null. Example: 0.00100000.
        paid_currency (None | str | Unset):  Example: BTC.
        payment_method (None | str | Unset):  Example: Btcpay.
    """

    id: int
    status: AffiliatePayoutStatus
    requested_amount: str
    requested_currency: str
    date_requested: datetime.datetime | None
    paid_amount: None | str | Unset = UNSET
    paid_currency: None | str | Unset = UNSET
    payment_method: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        requested_amount = self.requested_amount

        requested_currency = self.requested_currency

        date_requested: None | str
        if isinstance(self.date_requested, datetime.datetime):
            date_requested = self.date_requested.isoformat()
        else:
            date_requested = self.date_requested

        paid_amount: None | str | Unset
        if isinstance(self.paid_amount, Unset):
            paid_amount = UNSET
        else:
            paid_amount = self.paid_amount

        paid_currency: None | str | Unset
        if isinstance(self.paid_currency, Unset):
            paid_currency = UNSET
        else:
            paid_currency = self.paid_currency

        payment_method: None | str | Unset
        if isinstance(self.payment_method, Unset):
            payment_method = UNSET
        else:
            payment_method = self.payment_method

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "status": status,
                "requested_amount": requested_amount,
                "requested_currency": requested_currency,
                "date_requested": date_requested,
            }
        )
        if paid_amount is not UNSET:
            field_dict["paid_amount"] = paid_amount
        if paid_currency is not UNSET:
            field_dict["paid_currency"] = paid_currency
        if payment_method is not UNSET:
            field_dict["payment_method"] = payment_method

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = AffiliatePayoutStatus(d.pop("status"))

        requested_amount = d.pop("requested_amount")

        requested_currency = d.pop("requested_currency")

        def _parse_date_requested(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_requested_type_0 = datetime.datetime.fromisoformat(data)

                return date_requested_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_requested = _parse_date_requested(d.pop("date_requested"))

        def _parse_paid_amount(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        paid_amount = _parse_paid_amount(d.pop("paid_amount", UNSET))

        def _parse_paid_currency(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        paid_currency = _parse_paid_currency(d.pop("paid_currency", UNSET))

        def _parse_payment_method(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        payment_method = _parse_payment_method(d.pop("payment_method", UNSET))

        affiliate_payout = cls(
            id=id,
            status=status,
            requested_amount=requested_amount,
            requested_currency=requested_currency,
            date_requested=date_requested,
            paid_amount=paid_amount,
            paid_currency=paid_currency,
            payment_method=payment_method,
        )

        return affiliate_payout
