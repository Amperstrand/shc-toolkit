from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="AppliedPayment")


@_attrs_define
class AppliedPayment:
    """A transaction applied to an invoice (shown when inv_display_payments is enabled).

    Attributes:
        transaction_id (int):  Example: 88.
        type_ (str):  Example: other.
        type_name (None | str):  Example: Bitcoin.
        amount (str):  Example: 11.99.
        currency (str):  Example: USD.
        date_added (datetime.datetime | None):
        applied_date (datetime.datetime | None):
    """

    transaction_id: int
    type_: str
    type_name: None | str
    amount: str
    currency: str
    date_added: datetime.datetime | None
    applied_date: datetime.datetime | None

    def to_dict(self) -> dict[str, Any]:
        transaction_id = self.transaction_id

        type_ = self.type_

        type_name: None | str
        type_name = self.type_name

        amount = self.amount

        currency = self.currency

        date_added: None | str
        if isinstance(self.date_added, datetime.datetime):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        applied_date: None | str
        if isinstance(self.applied_date, datetime.datetime):
            applied_date = self.applied_date.isoformat()
        else:
            applied_date = self.applied_date

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "transaction_id": transaction_id,
                "type": type_,
                "type_name": type_name,
                "amount": amount,
                "currency": currency,
                "date_added": date_added,
                "applied_date": applied_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transaction_id = d.pop("transaction_id")

        type_ = d.pop("type")

        def _parse_type_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        type_name = _parse_type_name(d.pop("type_name"))

        amount = d.pop("amount")

        currency = d.pop("currency")

        def _parse_date_added(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_added_type_0 = datetime.datetime.fromisoformat(data)

                return date_added_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        date_added = _parse_date_added(d.pop("date_added"))

        def _parse_applied_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                applied_date_type_0 = datetime.datetime.fromisoformat(data)

                return applied_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        applied_date = _parse_applied_date(d.pop("applied_date"))

        applied_payment = cls(
            transaction_id=transaction_id,
            type_=type_,
            type_name=type_name,
            amount=amount,
            currency=currency,
            date_added=date_added,
            applied_date=applied_date,
        )

        return applied_payment
