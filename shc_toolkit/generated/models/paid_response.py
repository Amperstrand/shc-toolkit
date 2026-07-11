from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.paid_response_status import PaidResponseStatus

T = TypeVar("T", bound="PaidResponse")


@_attrs_define
class PaidResponse:
    """
    Example:
        {'status': 'paid', 'invoice_id': 1550, 'transaction_id': 8441, 'paid_at': '2026-05-05T22:03:11+00:00',
            'applied_credit': '11.99'}

    Attributes:
        status (PaidResponseStatus):  Example: paid.
        invoice_id (int):  Example: 1550.
        transaction_id (int | None): Blesta transaction row ID when one exists. Zero-value invoices may close without a
            backing transaction row. Example: 8441.
        paid_at (datetime.datetime):  Example: 2026-05-05T22:03:11+00:00.
        applied_credit (str): Amount of client credit applied by this call. `0.00` for zero-value invoices and already-
            paid invoices. Example: 11.99.
    """

    status: PaidResponseStatus
    invoice_id: int
    transaction_id: int | None
    paid_at: datetime.datetime
    applied_credit: str

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        invoice_id = self.invoice_id

        transaction_id: int | None
        transaction_id = self.transaction_id

        paid_at = self.paid_at.isoformat()

        applied_credit = self.applied_credit

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "invoice_id": invoice_id,
                "transaction_id": transaction_id,
                "paid_at": paid_at,
                "applied_credit": applied_credit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = PaidResponseStatus(d.pop("status"))

        invoice_id = d.pop("invoice_id")

        def _parse_transaction_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        transaction_id = _parse_transaction_id(d.pop("transaction_id"))

        paid_at = datetime.datetime.fromisoformat(d.pop("paid_at"))

        applied_credit = d.pop("applied_credit")

        paid_response = cls(
            status=status,
            invoice_id=invoice_id,
            transaction_id=transaction_id,
            paid_at=paid_at,
            applied_credit=applied_credit,
        )

        return paid_response
