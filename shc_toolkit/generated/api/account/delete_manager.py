from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_manager_response_200 import DeleteManagerResponse200
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    ref: str,
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
        "url": "/managers/{ref}".format(
            ref=quote(str(ref), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteManagerResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = DeleteManagerResponse200.from_dict(response.json())

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
) -> Response[DeleteManagerResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ref: str,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteManagerResponse200 | Error]:
    """Revoke a manager or cancel a manager invitation

     Revokes an active manager of this client (numeric `ref` = contact id) OR cancels a pending manager
    invitation this client issued (`ref` = invitation token). 404 existence-hiding when neither matches
    this client.

    Args:
        ref (str):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteManagerResponse200 | Error]
    """

    kwargs = _get_kwargs(
        ref=ref,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ref: str,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteManagerResponse200 | Error | None:
    """Revoke a manager or cancel a manager invitation

     Revokes an active manager of this client (numeric `ref` = contact id) OR cancels a pending manager
    invitation this client issued (`ref` = invitation token). 404 existence-hiding when neither matches
    this client.

    Args:
        ref (str):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteManagerResponse200 | Error
    """

    return sync_detailed(
        ref=ref,
        client=client,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    ref: str,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteManagerResponse200 | Error]:
    """Revoke a manager or cancel a manager invitation

     Revokes an active manager of this client (numeric `ref` = contact id) OR cancels a pending manager
    invitation this client issued (`ref` = invitation token). 404 existence-hiding when neither matches
    this client.

    Args:
        ref (str):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteManagerResponse200 | Error]
    """

    kwargs = _get_kwargs(
        ref=ref,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ref: str,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteManagerResponse200 | Error | None:
    """Revoke a manager or cancel a manager invitation

     Revokes an active manager of this client (numeric `ref` = contact id) OR cancels a pending manager
    invitation this client issued (`ref` = invitation token). 404 existence-hiding when neither matches
    this client.

    Args:
        ref (str):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteManagerResponse200 | Error
    """

    return (
        await asyncio_detailed(
            ref=ref,
            client=client,
            confirm=confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
