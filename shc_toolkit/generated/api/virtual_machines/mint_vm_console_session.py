from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.mint_vm_console_session_body import MintVmConsoleSessionBody
from ...models.mint_vm_console_session_response_201 import (
    MintVmConsoleSessionResponse201,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: MintVmConsoleSessionBody | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/console/session".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | MintVmConsoleSessionResponse201 | None:
    if response.status_code == 201:
        response_201 = MintVmConsoleSessionResponse201.from_dict(response.json())

        return response_201

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
) -> Response[Error | MintVmConsoleSessionResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: MintVmConsoleSessionBody | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | MintVmConsoleSessionResponse201]:
    """Mint a live console session

     Mints a single-use, short-TTL, VM-scoped noVNC console session for one owned, active VM whose node
    enables the console feature, and returns a ready-to-open console URL plus its expiry. STRICT PARITY
    with the portal console tab: it runs the same admin-side PVE flow (ephemeral per-VM PVE user limited
    to VM.Console, expiring in ~60s; vncproxy ticket) and routes through the same secure noVNC bridge.
    The URL carries a short-lived signed token in its fragment and is meant to be handed to a human to
    open in a browser. The response NEVER includes PVE admin credentials, the PVE auth ticket, the node
    name, or the underlying VM id.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (MintVmConsoleSessionBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MintVmConsoleSessionResponse201]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: MintVmConsoleSessionBody | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | MintVmConsoleSessionResponse201 | None:
    """Mint a live console session

     Mints a single-use, short-TTL, VM-scoped noVNC console session for one owned, active VM whose node
    enables the console feature, and returns a ready-to-open console URL plus its expiry. STRICT PARITY
    with the portal console tab: it runs the same admin-side PVE flow (ephemeral per-VM PVE user limited
    to VM.Console, expiring in ~60s; vncproxy ticket) and routes through the same secure noVNC bridge.
    The URL carries a short-lived signed token in its fragment and is meant to be handed to a human to
    open in a browser. The response NEVER includes PVE admin credentials, the PVE auth ticket, the node
    name, or the underlying VM id.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (MintVmConsoleSessionBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MintVmConsoleSessionResponse201
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: MintVmConsoleSessionBody | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | MintVmConsoleSessionResponse201]:
    """Mint a live console session

     Mints a single-use, short-TTL, VM-scoped noVNC console session for one owned, active VM whose node
    enables the console feature, and returns a ready-to-open console URL plus its expiry. STRICT PARITY
    with the portal console tab: it runs the same admin-side PVE flow (ephemeral per-VM PVE user limited
    to VM.Console, expiring in ~60s; vncproxy ticket) and routes through the same secure noVNC bridge.
    The URL carries a short-lived signed token in its fragment and is meant to be handed to a human to
    open in a browser. The response NEVER includes PVE admin credentials, the PVE auth ticket, the node
    name, or the underlying VM id.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (MintVmConsoleSessionBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MintVmConsoleSessionResponse201]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: MintVmConsoleSessionBody | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | MintVmConsoleSessionResponse201 | None:
    """Mint a live console session

     Mints a single-use, short-TTL, VM-scoped noVNC console session for one owned, active VM whose node
    enables the console feature, and returns a ready-to-open console URL plus its expiry. STRICT PARITY
    with the portal console tab: it runs the same admin-side PVE flow (ephemeral per-VM PVE user limited
    to VM.Console, expiring in ~60s; vncproxy ticket) and routes through the same secure noVNC bridge.
    The URL carries a short-lived signed token in its fragment and is meant to be handed to a human to
    open in a browser. The response NEVER includes PVE admin credentials, the PVE auth ticket, the node
    name, or the underlying VM id.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (MintVmConsoleSessionBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MintVmConsoleSessionResponse201
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
