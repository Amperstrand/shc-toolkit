from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.checkout_redirect_response_status import CheckoutRedirectResponseStatus

T = TypeVar("T", bound="CheckoutRedirectResponse")


@_attrs_define
class CheckoutRedirectResponse:
    """
    Example:
        {'status': 'checkout_required', 'checkout_url':
            'https://btcpay.sovereignhybridcompute.com/i/G7hYQdbfL3E7Pj7u5d7s2C', 'btcpay_invoice_id':
            'G7hYQdbfL3E7Pj7u5d7s2C', 'invoice_id': 1550, 'gateway': 'btcpay_server', 'expires_at':
            '2026-05-05T22:18:11+00:00'}

    Attributes:
        status (CheckoutRedirectResponseStatus):  Example: checkout_required.
        checkout_url (str):  Example: https://btcpay.sovereignhybridcompute.com/i/G7hYQdbfL3E7Pj7u5d7s2C.
        btcpay_invoice_id (str):  Example: G7hYQdbfL3E7Pj7u5d7s2C.
        invoice_id (int):  Example: 1550.
        gateway (str):  Example: btcpay_server.
        expires_at (datetime.datetime):  Example: 2026-05-05T22:18:11+00:00.
    """

    status: CheckoutRedirectResponseStatus
    checkout_url: str
    btcpay_invoice_id: str
    invoice_id: int
    gateway: str
    expires_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = CheckoutRedirectResponseStatus(d.pop("status"))

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
