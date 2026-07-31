from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.checkout_redirect_response_status import (
    CheckoutRedirectResponseStatus,
    check_checkout_redirect_response_status,
)

T = TypeVar("T", bound="CheckoutRedirectResponse")


@_attrs_define
class CheckoutRedirectResponse:
    """
    Example:
        {'status': 'checkout_required', 'checkout_url':
            'https://btcpay.sovereignhybridcompute.com/i/G7hYQdbfL3E7Pj7u5d7s2C', 'btcpay_invoice_id':
            'G7hYQdbfL3E7Pj7u5d7s2C', 'invoice_id': 1550, 'gateway': 'btcpay_server', 'expires_at':
            '2026-05-05T22:18:11+00:00'}

    """

    status: CheckoutRedirectResponseStatus
    checkout_url: str
    btcpay_invoice_id: str
    invoice_id: int
    gateway: str
    expires_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        checkout_url = self.checkout_url

        btcpay_invoice_id = self.btcpay_invoice_id

        invoice_id = self.invoice_id

        gateway = self.gateway

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "status": status,
                "checkout_url": checkout_url,
                "btcpay_invoice_id": btcpay_invoice_id,
                "invoice_id": invoice_id,
                "gateway": gateway,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = check_checkout_redirect_response_status(d.pop("status"))

        checkout_url = d.pop("checkout_url")

        btcpay_invoice_id = d.pop("btcpay_invoice_id")

        invoice_id = d.pop("invoice_id")

        gateway = d.pop("gateway")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        checkout_redirect_response = cls(
            status=status,
            checkout_url=checkout_url,
            btcpay_invoice_id=btcpay_invoice_id,
            invoice_id=invoice_id,
            gateway=gateway,
            expires_at=expires_at,
        )

        return checkout_redirect_response
