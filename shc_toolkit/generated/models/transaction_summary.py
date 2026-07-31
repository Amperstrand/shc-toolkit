from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.transaction_summary_status import (
    TransactionSummaryStatus,
    check_transaction_summary_status,
)
from ..models.transaction_summary_type import (
    TransactionSummaryType,
    check_transaction_summary_type,
)

T = TypeVar("T", bound="TransactionSummary")


@_attrs_define
class TransactionSummary:
    """Customer-safe transaction row (staff/internal columns stripped)."""

    id: int
    amount: str
    applied_amount: str
    currency: str
    type_: TransactionSummaryType
    type_name: None | str
    transaction_type_id: int | None
    status: TransactionSummaryStatus
    reference_id: None | str
    transaction_number: None | str
    message: None | str
    gateway_name: None | str
    date_added: datetime.datetime | None

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        amount = self.amount

        applied_amount = self.applied_amount

        currency = self.currency

        type_: str = self.type_

        type_name: None | str
        type_name = self.type_name

        transaction_type_id: int | None
        transaction_type_id = self.transaction_type_id

        status: str = self.status

        reference_id: None | str
        reference_id = self.reference_id

        transaction_number: None | str
        transaction_number = self.transaction_number

        message: None | str
        message = self.message

        gateway_name: None | str
        gateway_name = self.gateway_name

        date_added: None | str
        if isinstance(self.date_added, datetime.datetime):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "amount": amount,
                "applied_amount": applied_amount,
                "currency": currency,
                "type": type_,
                "type_name": type_name,
                "transaction_type_id": transaction_type_id,
                "status": status,
                "reference_id": reference_id,
                "transaction_number": transaction_number,
                "message": message,
                "gateway_name": gateway_name,
                "date_added": date_added,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        amount = d.pop("amount")

        applied_amount = d.pop("applied_amount")

        currency = d.pop("currency")

        type_ = check_transaction_summary_type(d.pop("type"))

        def _parse_type_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        type_name = _parse_type_name(d.pop("type_name"))

        def _parse_transaction_type_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        transaction_type_id = _parse_transaction_type_id(d.pop("transaction_type_id"))

        status = check_transaction_summary_status(d.pop("status"))

        def _parse_reference_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        reference_id = _parse_reference_id(d.pop("reference_id"))

        def _parse_transaction_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        transaction_number = _parse_transaction_number(d.pop("transaction_number"))

        def _parse_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        message = _parse_message(d.pop("message"))

        def _parse_gateway_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gateway_name = _parse_gateway_name(d.pop("gateway_name"))

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

        transaction_summary = cls(
            id=id,
            amount=amount,
            applied_amount=applied_amount,
            currency=currency,
            type_=type_,
            type_name=type_name,
            transaction_type_id=transaction_type_id,
            status=status,
            reference_id=reference_id,
            transaction_number=transaction_number,
            message=message,
            gateway_name=gateway_name,
            date_added=date_added,
        )

        return transaction_summary
