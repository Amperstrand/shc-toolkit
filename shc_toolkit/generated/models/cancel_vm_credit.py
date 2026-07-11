from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="CancelVmCredit")


@_attrs_define
class CancelVmCredit:
    """Financial outcome of an immediate cancellation. Only present on `immediate: true` responses. `issued: false` means
    the auto-credit was either zero (no unused-paid time) or that the in_house_credit transaction failed to land — check
    the customer's billing history for ground truth.

        Example:
            {'amount': 12.47, 'currency': 'USD', 'transaction_id': 8412, 'issued': True}

        Attributes:
            amount (float): Prorated unused-paid time credited to the customer's in-house balance (rounded ceil-to-cent so
                the customer is favored on rounding). Zero if no eligible paid term covered the cancellation moment. Example:
                12.47.
            currency (None | str): ISO-4217 currency code the credit was denominated in — derived from
                `clients.settings.default_currency`, which can differ from the original invoice currency for clients whose
                default has changed since paying. Example: USD.
            transaction_id (int | None): Blesta transaction id for the issued in_house_credit (transaction_type_id=4).
                `null` if no credit was issued (zero amount or remediation failure). Example: 8412.
            issued (bool): True only when an in_house_credit transaction was successfully recorded. Example: True.
    """

    amount: float
    currency: None | str
    transaction_id: int | None
    issued: bool

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        currency: None | str
        currency = self.currency

        transaction_id: int | None
        transaction_id = self.transaction_id

        issued = self.issued

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "amount": amount,
                "currency": currency,
                "transaction_id": transaction_id,
                "issued": issued,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount")

        def _parse_currency(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        currency = _parse_currency(d.pop("currency"))

        def _parse_transaction_id(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        transaction_id = _parse_transaction_id(d.pop("transaction_id"))

        issued = d.pop("issued")

        cancel_vm_credit = cls(
            amount=amount,
            currency=currency,
            transaction_id=transaction_id,
            issued=issued,
        )

        return cancel_vm_credit
