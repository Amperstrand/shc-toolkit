from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.affiliate_referral_status import AffiliateReferralStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AffiliateReferral")


@_attrs_define
class AffiliateReferral:
    """
    Attributes:
        id (int):  Example: 17.
        status (AffiliateReferralStatus):  Example: mature.
        amount (str): Invoiced order amount, BTC (8 dp). Example: 0.05000000.
        commission (str): Accrued commission, BTC (8 dp). Example: 0.00100000.
        currency (str):  Example: BTC.
        order_number (None | str | Unset):  Example: ORD-1042.
        date_added (datetime.datetime | None | Unset):
    """

    id: int
    status: AffiliateReferralStatus
    amount: str
    commission: str
    currency: str
    order_number: None | str | Unset = UNSET
    date_added: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        amount = self.amount

        commission = self.commission

        currency = self.currency

        order_number: None | str | Unset
        if isinstance(self.order_number, Unset):
            order_number = UNSET
        else:
            order_number = self.order_number

        date_added: None | str | Unset
        if isinstance(self.date_added, Unset):
            date_added = UNSET
        elif isinstance(self.date_added, datetime.datetime):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "status": status,
                "amount": amount,
                "commission": commission,
                "currency": currency,
            }
        )
        if order_number is not UNSET:
            field_dict["order_number"] = order_number
        if date_added is not UNSET:
            field_dict["date_added"] = date_added

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        status = AffiliateReferralStatus(d.pop("status"))

        amount = d.pop("amount")

        commission = d.pop("commission")

        currency = d.pop("currency")

        def _parse_order_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        order_number = _parse_order_number(d.pop("order_number", UNSET))

        def _parse_date_added(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_added_type_0 = datetime.datetime.fromisoformat(data)

                return date_added_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_added = _parse_date_added(d.pop("date_added", UNSET))

        affiliate_referral = cls(
            id=id,
            status=status,
            amount=amount,
            commission=commission,
            currency=currency,
            order_number=order_number,
            date_added=date_added,
        )

        return affiliate_referral
