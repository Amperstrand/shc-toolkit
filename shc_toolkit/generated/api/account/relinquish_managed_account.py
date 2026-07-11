from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.relinquish_managed_account_response_200 import (
    RelinquishManagedAccountResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    managed_client_id: int,
    *,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["confirm"] = confirm

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/managed-accounts/{managed_client_id}".format(
            managed_client_id=quote(str(managed_client_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | RelinquishManagedAccountResponse200 | None:
    if response.status_code == 200:
        response_200 = RelinquishManagedAccountResponse200.from_dict(response.json())

        return response_200

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
) -> Response[Error | RelinquishManagedAccountResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    managed_client_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | RelinquishManagedAccountResponse200]:
    """Relinquish a managed account

     Gives up managing an account the authenticated client currently manages. 404 existence-hiding when
    the client does not manage that account.

    Args:
        managed_client_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RelinquishManagedAccountResponse200]
    """

    kwargs = _get_kwargs(
        managed_client_id=managed_client_id,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    managed_client_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | RelinquishManagedAccountResponse200 | None:
    """Relinquish a managed account

     Gives up managing an account the authenticated client currently manages. 404 existence-hiding when
    the client does not manage that account.

    Args:
        managed_client_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RelinquishManagedAccountResponse200
    """

    return sync_detailed(
        managed_client_id=managed_client_id,
        client=client,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    managed_client_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | RelinquishManagedAccountResponse200]:
    """Relinquish a managed account

     Gives up managing an account the authenticated client currently manages. 404 existence-hiding when
    the client does not manage that account.

    Args:
        managed_client_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RelinquishManagedAccountResponse200]
    """

    kwargs = _get_kwargs(
        managed_client_id=managed_client_id,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    managed_client_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | RelinquishManagedAccountResponse200 | None:
    """Relinquish a managed account

     Gives up managing an account the authenticated client currently manages. 404 existence-hiding when
    the client does not manage that account.

    Args:
        managed_client_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RelinquishManagedAccountResponse200
    """

    return (
        await asyncio_detailed(
            managed_client_id=managed_client_id,
            client=client,
            confirm=confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
