from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_billing_balance_response_200 import GetBillingBalanceResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    currency: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["currency"] = currency

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/billing/balance",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetBillingBalanceResponse200 | None:
    if response.status_code == 200:
        response_200 = GetBillingBalanceResponse200.from_dict(response.json())

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

    if response.status_code == 405:
        response_405 = Error.from_dict(response.json())

        return response_405

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | GetBillingBalanceResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    currency: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetBillingBalanceResponse200]:
    """Get account balance and available credit

     Per-currency account balance for the authenticated client. `available_credit` mirrors the portal
    Total Credits figure; `balance_due` is aggregated from the same open-invoice filter that backs `GET
    /invoices?status=open`. Reports figures only; moves no money. Self-scoped read (the portal gates the
    sidebar on a per-client permission the API does not model — an authenticated client always reads
    their own credit).

    Args:
        currency (str | Unset):  Example: USD.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetBillingBalanceResponse200]
    """

    kwargs = _get_kwargs(
        currency=currency,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    currency: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetBillingBalanceResponse200 | None:
    """Get account balance and available credit

     Per-currency account balance for the authenticated client. `available_credit` mirrors the portal
    Total Credits figure; `balance_due` is aggregated from the same open-invoice filter that backs `GET
    /invoices?status=open`. Reports figures only; moves no money. Self-scoped read (the portal gates the
    sidebar on a per-client permission the API does not model — an authenticated client always reads
    their own credit).

    Args:
        currency (str | Unset):  Example: USD.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetBillingBalanceResponse200
    """

    return sync_detailed(
        client=client,
        currency=currency,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    currency: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetBillingBalanceResponse200]:
    """Get account balance and available credit

     Per-currency account balance for the authenticated client. `available_credit` mirrors the portal
    Total Credits figure; `balance_due` is aggregated from the same open-invoice filter that backs `GET
    /invoices?status=open`. Reports figures only; moves no money. Self-scoped read (the portal gates the
    sidebar on a per-client permission the API does not model — an authenticated client always reads
    their own credit).

    Args:
        currency (str | Unset):  Example: USD.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetBillingBalanceResponse200]
    """

    kwargs = _get_kwargs(
        currency=currency,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    currency: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetBillingBalanceResponse200 | None:
    """Get account balance and available credit

     Per-currency account balance for the authenticated client. `available_credit` mirrors the portal
    Total Credits figure; `balance_due` is aggregated from the same open-invoice filter that backs `GET
    /invoices?status=open`. Reports figures only; moves no money. Self-scoped read (the portal gates the
    sidebar on a per-client permission the API does not model — an authenticated client always reads
    their own credit).

    Args:
        currency (str | Unset):  Example: USD.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetBillingBalanceResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            currency=currency,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
