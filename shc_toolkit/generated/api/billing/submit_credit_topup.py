from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.credit_topup_request import CreditTopupRequest
from ...models.error import Error
from ...models.submit_credit_topup_response_200 import SubmitCreditTopupResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: CreditTopupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/account/credit",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | SubmitCreditTopupResponse200 | None:
    if response.status_code == 200:
        response_200 = SubmitCreditTopupResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

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

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

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
) -> Response[Error | SubmitCreditTopupResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreditTopupRequest,
) -> Response[Error | SubmitCreditTopupResponse200]:
    """Add account credit (top up) via BTCPay

     Mints a BTCPay payment with NO invoice attached, so the settled funds become unapplied **account
    credit** — the API equivalent of the customer portal's *Add Funds*. Returns a hosted `checkout_url`
    and, when available, a **BOLT11 Lightning invoice** (`bolt11`) and on-chain address so a wallet or
    automation can pay directly. Requires a full-scope customer API key or Basic+OTP; operate-scoped
    keys are rejected (this is a money-movement route, so an operate key cannot spend). The `amount`
    must be a positive decimal with at most 2 places (no rounding). Idempotent on the body
    `idempotency_key`. The credit lands once the BTCPay payment confirms (via webhook).

    Args:
        body (CreditTopupRequest):  Example: {'amount': '25.00', 'currency': 'USD',
            'idempotency_key': '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SubmitCreditTopupResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreditTopupRequest,
) -> Error | SubmitCreditTopupResponse200 | None:
    """Add account credit (top up) via BTCPay

     Mints a BTCPay payment with NO invoice attached, so the settled funds become unapplied **account
    credit** — the API equivalent of the customer portal's *Add Funds*. Returns a hosted `checkout_url`
    and, when available, a **BOLT11 Lightning invoice** (`bolt11`) and on-chain address so a wallet or
    automation can pay directly. Requires a full-scope customer API key or Basic+OTP; operate-scoped
    keys are rejected (this is a money-movement route, so an operate key cannot spend). The `amount`
    must be a positive decimal with at most 2 places (no rounding). Idempotent on the body
    `idempotency_key`. The credit lands once the BTCPay payment confirms (via webhook).

    Args:
        body (CreditTopupRequest):  Example: {'amount': '25.00', 'currency': 'USD',
            'idempotency_key': '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SubmitCreditTopupResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreditTopupRequest,
) -> Response[Error | SubmitCreditTopupResponse200]:
    """Add account credit (top up) via BTCPay

     Mints a BTCPay payment with NO invoice attached, so the settled funds become unapplied **account
    credit** — the API equivalent of the customer portal's *Add Funds*. Returns a hosted `checkout_url`
    and, when available, a **BOLT11 Lightning invoice** (`bolt11`) and on-chain address so a wallet or
    automation can pay directly. Requires a full-scope customer API key or Basic+OTP; operate-scoped
    keys are rejected (this is a money-movement route, so an operate key cannot spend). The `amount`
    must be a positive decimal with at most 2 places (no rounding). Idempotent on the body
    `idempotency_key`. The credit lands once the BTCPay payment confirms (via webhook).

    Args:
        body (CreditTopupRequest):  Example: {'amount': '25.00', 'currency': 'USD',
            'idempotency_key': '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SubmitCreditTopupResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreditTopupRequest,
) -> Error | SubmitCreditTopupResponse200 | None:
    """Add account credit (top up) via BTCPay

     Mints a BTCPay payment with NO invoice attached, so the settled funds become unapplied **account
    credit** — the API equivalent of the customer portal's *Add Funds*. Returns a hosted `checkout_url`
    and, when available, a **BOLT11 Lightning invoice** (`bolt11`) and on-chain address so a wallet or
    automation can pay directly. Requires a full-scope customer API key or Basic+OTP; operate-scoped
    keys are rejected (this is a money-movement route, so an operate key cannot spend). The `amount`
    must be a positive decimal with at most 2 places (no rounding). Idempotent on the body
    `idempotency_key`. The credit lands once the BTCPay payment confirms (via webhook).

    Args:
        body (CreditTopupRequest):  Example: {'amount': '25.00', 'currency': 'USD',
            'idempotency_key': '5f051e42-f6a0-4f4d-9b67-c444f4673dd7'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SubmitCreditTopupResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
