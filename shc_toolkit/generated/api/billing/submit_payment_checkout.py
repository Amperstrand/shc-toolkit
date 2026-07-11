from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.payment_checkout_request import PaymentCheckoutRequest
from ...models.submit_payment_checkout_response_200 import (
    SubmitPaymentCheckoutResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    invoice_id: int,
    *,
    body: PaymentCheckoutRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/payment/{invoice_id}/checkout".format(
            invoice_id=quote(str(invoice_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | SubmitPaymentCheckoutResponse200 | None:
    if response.status_code == 200:
        response_200 = SubmitPaymentCheckoutResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 405:
        response_405 = Error.from_dict(response.json())

        return response_405

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())

        return response_502

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | SubmitPaymentCheckoutResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    invoice_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PaymentCheckoutRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SubmitPaymentCheckoutResponse200]:
    """Create or replay a BTCPay checkout for an owned invoice

     Creates a BTCPay checkout through Blesta's existing nonmerchant gateway flow for an owned open
    invoice. The request body carries the required `idempotency_key`. Reusing the same key with the same
    canonical body for the same invoice within 24 hours replays the original `200` response; reusing it
    with a different body returns `409 idempotency_key_in_use`.

    Args:
        invoice_id (int):
        x_user_api_otp (str | Unset):
        body (PaymentCheckoutRequest):  Example: {'gateway': 'btcpay_server', 'idempotency_key':
            '5f051e42-f6a0-4f4d-9b67-c444f4673dd7', 'return_url':
            'https://app.example.com/billing/return', 'cancel_url':
            'https://app.example.com/billing/cancel'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SubmitPaymentCheckoutResponse200]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    invoice_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PaymentCheckoutRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SubmitPaymentCheckoutResponse200 | None:
    """Create or replay a BTCPay checkout for an owned invoice

     Creates a BTCPay checkout through Blesta's existing nonmerchant gateway flow for an owned open
    invoice. The request body carries the required `idempotency_key`. Reusing the same key with the same
    canonical body for the same invoice within 24 hours replays the original `200` response; reusing it
    with a different body returns `409 idempotency_key_in_use`.

    Args:
        invoice_id (int):
        x_user_api_otp (str | Unset):
        body (PaymentCheckoutRequest):  Example: {'gateway': 'btcpay_server', 'idempotency_key':
            '5f051e42-f6a0-4f4d-9b67-c444f4673dd7', 'return_url':
            'https://app.example.com/billing/return', 'cancel_url':
            'https://app.example.com/billing/cancel'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SubmitPaymentCheckoutResponse200
    """

    return sync_detailed(
        invoice_id=invoice_id,
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    invoice_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PaymentCheckoutRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SubmitPaymentCheckoutResponse200]:
    """Create or replay a BTCPay checkout for an owned invoice

     Creates a BTCPay checkout through Blesta's existing nonmerchant gateway flow for an owned open
    invoice. The request body carries the required `idempotency_key`. Reusing the same key with the same
    canonical body for the same invoice within 24 hours replays the original `200` response; reusing it
    with a different body returns `409 idempotency_key_in_use`.

    Args:
        invoice_id (int):
        x_user_api_otp (str | Unset):
        body (PaymentCheckoutRequest):  Example: {'gateway': 'btcpay_server', 'idempotency_key':
            '5f051e42-f6a0-4f4d-9b67-c444f4673dd7', 'return_url':
            'https://app.example.com/billing/return', 'cancel_url':
            'https://app.example.com/billing/cancel'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SubmitPaymentCheckoutResponse200]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    invoice_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PaymentCheckoutRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SubmitPaymentCheckoutResponse200 | None:
    """Create or replay a BTCPay checkout for an owned invoice

     Creates a BTCPay checkout through Blesta's existing nonmerchant gateway flow for an owned open
    invoice. The request body carries the required `idempotency_key`. Reusing the same key with the same
    canonical body for the same invoice within 24 hours replays the original `200` response; reusing it
    with a different body returns `409 idempotency_key_in_use`.

    Args:
        invoice_id (int):
        x_user_api_otp (str | Unset):
        body (PaymentCheckoutRequest):  Example: {'gateway': 'btcpay_server', 'idempotency_key':
            '5f051e42-f6a0-4f4d-9b67-c444f4673dd7', 'return_url':
            'https://app.example.com/billing/return', 'cancel_url':
            'https://app.example.com/billing/cancel'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SubmitPaymentCheckoutResponse200
    """

    return (
        await asyncio_detailed(
            invoice_id=invoice_id,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
