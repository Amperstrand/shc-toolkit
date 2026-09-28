from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_quotations_response_200 import ListQuotationsResponse200
from ...models.list_quotations_status import ListQuotationsStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListQuotationsStatus | Unset = ListQuotationsStatus.PENDING,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/quotations",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListQuotationsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListQuotationsResponse200.from_dict(response.json())

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
) -> Response[Error | ListQuotationsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListQuotationsStatus | Unset = ListQuotationsStatus.PENDING,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListQuotationsResponse200]:
    """List the client's quotations

     Lists the authenticated customer's quotations, client-scoped, with an optional status filter.
    Defaults to pending.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        status (ListQuotationsStatus | Unset):  Default: ListQuotationsStatus.PENDING.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListQuotationsResponse200]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        status=status,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListQuotationsStatus | Unset = ListQuotationsStatus.PENDING,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListQuotationsResponse200 | None:
    """List the client's quotations

     Lists the authenticated customer's quotations, client-scoped, with an optional status filter.
    Defaults to pending.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        status (ListQuotationsStatus | Unset):  Default: ListQuotationsStatus.PENDING.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListQuotationsResponse200
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        status=status,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListQuotationsStatus | Unset = ListQuotationsStatus.PENDING,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListQuotationsResponse200]:
    """List the client's quotations

     Lists the authenticated customer's quotations, client-scoped, with an optional status filter.
    Defaults to pending.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        status (ListQuotationsStatus | Unset):  Default: ListQuotationsStatus.PENDING.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListQuotationsResponse200]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        status=status,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    status: ListQuotationsStatus | Unset = ListQuotationsStatus.PENDING,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListQuotationsResponse200 | None:
    """List the client's quotations

     Lists the authenticated customer's quotations, client-scoped, with an optional status filter.
    Defaults to pending.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        status (ListQuotationsStatus | Unset):  Default: ListQuotationsStatus.PENDING.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListQuotationsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            status=status,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
