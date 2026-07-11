from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_orders_response_200 import ListOrdersResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    status: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["status"] = status

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/orders",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListOrdersResponse200 | None:
    if response.status_code == 200:
        response_200 = ListOrdersResponse200.from_dict(response.json())

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | ListOrdersResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    status: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListOrdersResponse200]:
    """List orders visible to the authenticated account, including pending orders

     List orders visible to the authenticated account, including pending orders. Staged parity op:
    declared in the canonical 2.5 surface; handler lands separately (release_state=staged until then).

    Args:
        status (str | Unset):
        limit (int | Unset):
        offset (int | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListOrdersResponse200]
    """

    kwargs = _get_kwargs(
        status=status,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    status: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListOrdersResponse200 | None:
    """List orders visible to the authenticated account, including pending orders

     List orders visible to the authenticated account, including pending orders. Staged parity op:
    declared in the canonical 2.5 surface; handler lands separately (release_state=staged until then).

    Args:
        status (str | Unset):
        limit (int | Unset):
        offset (int | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListOrdersResponse200
    """

    return sync_detailed(
        client=client,
        status=status,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    status: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListOrdersResponse200]:
    """List orders visible to the authenticated account, including pending orders

     List orders visible to the authenticated account, including pending orders. Staged parity op:
    declared in the canonical 2.5 surface; handler lands separately (release_state=staged until then).

    Args:
        status (str | Unset):
        limit (int | Unset):
        offset (int | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListOrdersResponse200]
    """

    kwargs = _get_kwargs(
        status=status,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    status: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    offset: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListOrdersResponse200 | None:
    """List orders visible to the authenticated account, including pending orders

     List orders visible to the authenticated account, including pending orders. Staged parity op:
    declared in the canonical 2.5 surface; handler lands separately (release_state=staged until then).

    Args:
        status (str | Unset):
        limit (int | Unset):
        offset (int | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListOrdersResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            status=status,
            limit=limit,
            offset=offset,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
