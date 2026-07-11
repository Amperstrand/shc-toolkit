from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreditTopupRequest")


@_attrs_define
class CreditTopupRequest:
    """
    Example:
        {'amount': '25.00', 'currency': 'USD', 'idempotency_key': '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}

    Attributes:
        amount (int | str): Amount of account credit to add. Send a positive decimal STRING with at most 2 decimal
            places (e.g. "25.00"); a bare integer is also accepted. A JSON float is REJECTED (422) so the customer is
            charged EXACTLY what they type — no silent rounding. Must be > 0 and within the account's configured credit
            limits. Example: 25.00.
        idempotency_key (str): REQUIRED client-supplied idempotency key (body field). Reuse the same value with the same
            body to replay the original response instead of minting a second top-up invoice. Example:
            5f051e42-f6a0-4f4d-9b67-c444f4673dd7.
        currency (str | Unset): Optional ISO-4217 code (defaults to the client's currency). Must be an active company
            currency. Example: USD.
        return_url (None | str | Unset): Optional HTTPS URL BTCPay redirects the browser to after payment. Non-https or
            non-allowlisted hosts are rejected with 400. Example: https://www.sovereignhybridcompute.com/account.
    """

    amount: int | str
    idempotency_key: str
    currency: str | Unset = UNSET
    return_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount: int | str
        amount = self.amount

        idempotency_key = self.idempotency_key

        currency = self.currency

        return_url: None | str | Unset
        if isinstance(self.return_url, Unset):
            return_url = UNSET
        else:
            return_url = self.return_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "idempotency_key": idempotency_key,
            }
        )
        if currency is not UNSET:
            field_dict["currency"] = currency
        if return_url is not UNSET:
            field_dict["return_url"] = return_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_amount(data: object) -> int | str:
            return cast(int | str, data)

        amount = _parse_amount(d.pop("amount"))

        idempotency_key = d.pop("idempotency_key")

        currency = d.pop("currency", UNSET)

        def _parse_return_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        return_url = _parse_return_url(d.pop("return_url", UNSET))

        credit_topup_request = cls(
            amount=amount,
            idempotency_key=idempotency_key,
            currency=currency,
            return_url=return_url,
        )

        credit_topup_request.additional_properties = d
        return credit_topup_request

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
