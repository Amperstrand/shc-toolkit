from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_api_keys_response_200 import ListApiKeysResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/account/api-keys",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListApiKeysResponse200 | None:
    if response.status_code == 200:
        response_200 = ListApiKeysResponse200.from_dict(response.json())

        return response_200

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
) -> Response[Error | ListApiKeysResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Error | ListApiKeysResponse200]:
    """List your active API keys (metadata only — never the key).

     v2.4.0: a FULL-scope customer API key may also call this LIST (key METADATA only — name, prefix,
    expiry, last_used; never the secret). Mint (POST) and revoke (DELETE) remain Basic+OTP only (anti-
    escalation).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListApiKeysResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Error | ListApiKeysResponse200 | None:
    """List your active API keys (metadata only — never the key).

     v2.4.0: a FULL-scope customer API key may also call this LIST (key METADATA only — name, prefix,
    expiry, last_used; never the secret). Mint (POST) and revoke (DELETE) remain Basic+OTP only (anti-
    escalation).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListApiKeysResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Error | ListApiKeysResponse200]:
    """List your active API keys (metadata only — never the key).

     v2.4.0: a FULL-scope customer API key may also call this LIST (key METADATA only — name, prefix,
    expiry, last_used; never the secret). Mint (POST) and revoke (DELETE) remain Basic+OTP only (anti-
    escalation).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListApiKeysResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Error | ListApiKeysResponse200 | None:
    """List your active API keys (metadata only — never the key).

     v2.4.0: a FULL-scope customer API key may also call this LIST (key METADATA only — name, prefix,
    expiry, last_used; never the secret). Mint (POST) and revoke (DELETE) remain Basic+OTP only (anti-
    escalation).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListApiKeysResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
