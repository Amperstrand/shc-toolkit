from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.credit_topup_response_status import CreditTopupResponseStatus
from ..models.credit_topup_response_type import CreditTopupResponseType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreditTopupResponse")


@_attrs_define
class CreditTopupResponse:
    """
    Attributes:
        status (CreditTopupResponseStatus):  Example: checkout_required.
        type_ (CreditTopupResponseType):  Example: account_credit.
        amount (str): The credited amount as a 2-decimal string. Example: 25.00.
        currency (str):  Example: USD.
        checkout_url (str): BTCPay hosted checkout page (pay by Lightning or on-chain in a browser). Example:
            https://btcpay.sovereignhybridcompute.com/i/G7hYQdbfL3E7Pj7u5d7s2C.
        bolt11 (None | str | Unset): A BOLT11 Lightning invoice for the amount, for wallets/automation that pay without
            the hosted page. Null if a direct Lightning invoice is unavailable for this invoice. Example:
            lnbc15900n1p4ztufspp5....
        onchain_address (None | str | Unset): On-chain Bitcoin address, when the store offers on-chain. Null on a
            Lightning-only store.
        payment_link (None | str | Unset): A single wallet-openable payment URI (prefers lightning:lnbc…, else
            lightning:lnurl…, else bitcoin:…). Example: lightning:lnbc15900n1p....
        expires_at (datetime.datetime | None | Unset): When the BTCPay invoice expires. Example:
            2026-06-07T22:46:11+00:00.
    """

    status: CreditTopupResponseStatus
    type_: CreditTopupResponseType
    amount: str
    currency: str
    checkout_url: str
    bolt11: None | str | Unset = UNSET
    onchain_address: None | str | Unset = UNSET
    payment_link: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        type_ = self.type_.value

        amount = self.amount

        currency = self.currency

        checkout_url = self.checkout_url

        bolt11: None | str | Unset
        if isinstance(self.bolt11, Unset):
            bolt11 = UNSET
        else:
            bolt11 = self.bolt11

        onchain_address: None | str | Unset
        if isinstance(self.onchain_address, Unset):
            onchain_address = UNSET
        else:
            onchain_address = self.onchain_address

        payment_link: None | str | Unset
        if isinstance(self.payment_link, Unset):
            payment_link = UNSET
        else:
            payment_link = self.payment_link

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "type": type_,
                "amount": amount,
                "currency": currency,
                "checkout_url": checkout_url,
            }
        )
        if bolt11 is not UNSET:
            field_dict["bolt11"] = bolt11
        if onchain_address is not UNSET:
            field_dict["onchain_address"] = onchain_address
        if payment_link is not UNSET:
            field_dict["payment_link"] = payment_link
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = CreditTopupResponseStatus(d.pop("status"))

        type_ = CreditTopupResponseType(d.pop("type"))

        amount = d.pop("amount")

        currency = d.pop("currency")

        checkout_url = d.pop("checkout_url")

        def _parse_bolt11(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        bolt11 = _parse_bolt11(d.pop("bolt11", UNSET))

        def _parse_onchain_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        onchain_address = _parse_onchain_address(d.pop("onchain_address", UNSET))

        def _parse_payment_link(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        payment_link = _parse_payment_link(d.pop("payment_link", UNSET))

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        credit_topup_response = cls(
            status=status,
            type_=type_,
            amount=amount,
            currency=currency,
            checkout_url=checkout_url,
            bolt11=bolt11,
            onchain_address=onchain_address,
            payment_link=payment_link,
            expires_at=expires_at,
        )

        return credit_topup_response
