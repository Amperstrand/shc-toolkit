from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.update_nip_05_body import UpdateNip05Body
from ...models.update_nip_05_response_200 import UpdateNip05Response200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: UpdateNip05Body,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/account/nostr/nip05",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UpdateNip05Response200 | None:
    if response.status_code == 200:
        response_200 = UpdateNip05Response200.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | UpdateNip05Response200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: UpdateNip05Body,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateNip05Response200]:
    """Update the NIP-05 identifier for the linked Nostr identity (Basic+OTP only)

     Update the linked Nostr identity's NIP-05 local name using the live /v2 nip05_name body field.

    Args:
        x_user_api_otp (str | Unset):
        body (UpdateNip05Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateNip05Response200]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: UpdateNip05Body,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateNip05Response200 | None:
    """Update the NIP-05 identifier for the linked Nostr identity (Basic+OTP only)

     Update the linked Nostr identity's NIP-05 local name using the live /v2 nip05_name body field.

    Args:
        x_user_api_otp (str | Unset):
        body (UpdateNip05Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateNip05Response200
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: UpdateNip05Body,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateNip05Response200]:
    """Update the NIP-05 identifier for the linked Nostr identity (Basic+OTP only)

     Update the linked Nostr identity's NIP-05 local name using the live /v2 nip05_name body field.

    Args:
        x_user_api_otp (str | Unset):
        body (UpdateNip05Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateNip05Response200]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: UpdateNip05Body,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateNip05Response200 | None:
    """Update the NIP-05 identifier for the linked Nostr identity (Basic+OTP only)

     Update the linked Nostr identity's NIP-05 local name using the live /v2 nip05_name body field.

    Args:
        x_user_api_otp (str | Unset):
        body (UpdateNip05Body):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateNip05Response200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
