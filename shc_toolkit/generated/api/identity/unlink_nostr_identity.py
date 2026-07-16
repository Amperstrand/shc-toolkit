from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.unlink_nostr_identity_body import UnlinkNostrIdentityBody
from ...models.unlink_nostr_identity_response_200 import UnlinkNostrIdentityResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: UnlinkNostrIdentityBody,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/account/nostr/unlink",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UnlinkNostrIdentityResponse200 | None:
    if response.status_code == 200:
        response_200 = UnlinkNostrIdentityResponse200.from_dict(response.json())

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
) -> Response[Error | UnlinkNostrIdentityResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: UnlinkNostrIdentityBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UnlinkNostrIdentityResponse200]:
    """Unlink the Nostr identity from the authenticated account (Basic+OTP only)

     Unlink the authenticated client's Nostr identity using a signed challenge event from the currently
    linked key.

    Args:
        x_user_api_otp (str | Unset):
        body (UnlinkNostrIdentityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UnlinkNostrIdentityResponse200]
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
    body: UnlinkNostrIdentityBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UnlinkNostrIdentityResponse200 | None:
    """Unlink the Nostr identity from the authenticated account (Basic+OTP only)

     Unlink the authenticated client's Nostr identity using a signed challenge event from the currently
    linked key.

    Args:
        x_user_api_otp (str | Unset):
        body (UnlinkNostrIdentityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UnlinkNostrIdentityResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: UnlinkNostrIdentityBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UnlinkNostrIdentityResponse200]:
    """Unlink the Nostr identity from the authenticated account (Basic+OTP only)

     Unlink the authenticated client's Nostr identity using a signed challenge event from the currently
    linked key.

    Args:
        x_user_api_otp (str | Unset):
        body (UnlinkNostrIdentityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UnlinkNostrIdentityResponse200]
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
    body: UnlinkNostrIdentityBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UnlinkNostrIdentityResponse200 | None:
    """Unlink the Nostr identity from the authenticated account (Basic+OTP only)

     Unlink the authenticated client's Nostr identity using a signed challenge event from the currently
    linked key.

    Args:
        x_user_api_otp (str | Unset):
        body (UnlinkNostrIdentityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UnlinkNostrIdentityResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
