from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_transaction_response_200 import GetTransactionResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    transaction_id: int,
    *,
    applied_limit: int | Unset = 100,
    applied_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["applied.limit"] = applied_limit

    params["applied.offset"] = applied_offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/transactions/{transaction_id}".format(
            transaction_id=quote(str(transaction_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetTransactionResponse200 | None:
    if response.status_code == 200:
        response_200 = GetTransactionResponse200.from_dict(response.json())

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
) -> Response[Error | GetTransactionResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    transaction_id: int,
    *,
    client: AuthenticatedClient | Client,
    applied_limit: int | Unset = 100,
    applied_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetTransactionResponse200]:
    """Get transaction detail

     Single transaction with a paginated list of the invoices it was applied to. Ownership is enforced at
    the SQL layer before any applied-invoice join.

    Args:
        transaction_id (int):
        applied_limit (int | Unset):  Default: 100.
        applied_offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetTransactionResponse200]
    """

    kwargs = _get_kwargs(
        transaction_id=transaction_id,
        applied_limit=applied_limit,
        applied_offset=applied_offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    transaction_id: int,
    *,
    client: AuthenticatedClient | Client,
    applied_limit: int | Unset = 100,
    applied_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetTransactionResponse200 | None:
    """Get transaction detail

     Single transaction with a paginated list of the invoices it was applied to. Ownership is enforced at
    the SQL layer before any applied-invoice join.

    Args:
        transaction_id (int):
        applied_limit (int | Unset):  Default: 100.
        applied_offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetTransactionResponse200
    """

    return sync_detailed(
        transaction_id=transaction_id,
        client=client,
        applied_limit=applied_limit,
        applied_offset=applied_offset,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    transaction_id: int,
    *,
    client: AuthenticatedClient | Client,
    applied_limit: int | Unset = 100,
    applied_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetTransactionResponse200]:
    """Get transaction detail

     Single transaction with a paginated list of the invoices it was applied to. Ownership is enforced at
    the SQL layer before any applied-invoice join.

    Args:
        transaction_id (int):
        applied_limit (int | Unset):  Default: 100.
        applied_offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetTransactionResponse200]
    """

    kwargs = _get_kwargs(
        transaction_id=transaction_id,
        applied_limit=applied_limit,
        applied_offset=applied_offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    transaction_id: int,
    *,
    client: AuthenticatedClient | Client,
    applied_limit: int | Unset = 100,
    applied_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetTransactionResponse200 | None:
    """Get transaction detail

     Single transaction with a paginated list of the invoices it was applied to. Ownership is enforced at
    the SQL layer before any applied-invoice join.

    Args:
        transaction_id (int):
        applied_limit (int | Unset):  Default: 100.
        applied_offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetTransactionResponse200
    """

    return (
        await asyncio_detailed(
            transaction_id=transaction_id,
            client=client,
            applied_limit=applied_limit,
            applied_offset=applied_offset,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
