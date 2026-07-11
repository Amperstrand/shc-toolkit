from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.ssh_key_entry_list import SshKeyEntryList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    service_id: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["service_id"] = service_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ssh-key",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | SshKeyEntryList | None:
    if response.status_code == 200:
        response_200 = SshKeyEntryList.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

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
) -> Response[Error | SshKeyEntryList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    service_id: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SshKeyEntryList]:
    """List stored SSH keys

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        service_id (int | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SshKeyEntryList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        service_id=service_id,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    service_id: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SshKeyEntryList | None:
    """List stored SSH keys

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        service_id (int | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SshKeyEntryList
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        service_id=service_id,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    service_id: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SshKeyEntryList]:
    """List stored SSH keys

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        service_id (int | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SshKeyEntryList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        service_id=service_id,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    service_id: int | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SshKeyEntryList | None:
    """List stored SSH keys

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        service_id (int | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SshKeyEntryList
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            service_id=service_id,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
