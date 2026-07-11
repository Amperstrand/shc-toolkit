from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.claim_agent_key_body import ClaimAgentKeyBody
from ...models.claim_agent_key_response_200 import ClaimAgentKeyResponse200
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: ClaimAgentKeyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agent-keys/claim",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClaimAgentKeyResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = ClaimAgentKeyResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

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
) -> Response[ClaimAgentKeyResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ClaimAgentKeyBody,
) -> Response[ClaimAgentKeyResponse200 | Error]:
    """Claim a single-use agent API key by claim code

     Public (unauthenticated) claim endpoint for operator-issued agent keys. The customer (or SHC on
    their behalf) mints a key and hands the AGENT only a single-use claim code; the agent exchanges the
    code here exactly once and receives the plaintext key (never recoverable again). Anti-enumeration:
    every existence-type miss (unknown / expired / already-claimed / raced) returns one uniform 404 body
    on a uniform response-time floor. Malformed requests are 422. Rate limited per source IP (30/10min)
    and per code (10/10min). NOT exposed as an MCP tool (public credential bootstrap; the MCP surface is
    authenticated).

    Args:
        body (ClaimAgentKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClaimAgentKeyResponse200 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ClaimAgentKeyBody,
) -> ClaimAgentKeyResponse200 | Error | None:
    """Claim a single-use agent API key by claim code

     Public (unauthenticated) claim endpoint for operator-issued agent keys. The customer (or SHC on
    their behalf) mints a key and hands the AGENT only a single-use claim code; the agent exchanges the
    code here exactly once and receives the plaintext key (never recoverable again). Anti-enumeration:
    every existence-type miss (unknown / expired / already-claimed / raced) returns one uniform 404 body
    on a uniform response-time floor. Malformed requests are 422. Rate limited per source IP (30/10min)
    and per code (10/10min). NOT exposed as an MCP tool (public credential bootstrap; the MCP surface is
    authenticated).

    Args:
        body (ClaimAgentKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClaimAgentKeyResponse200 | Error
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ClaimAgentKeyBody,
) -> Response[ClaimAgentKeyResponse200 | Error]:
    """Claim a single-use agent API key by claim code

     Public (unauthenticated) claim endpoint for operator-issued agent keys. The customer (or SHC on
    their behalf) mints a key and hands the AGENT only a single-use claim code; the agent exchanges the
    code here exactly once and receives the plaintext key (never recoverable again). Anti-enumeration:
    every existence-type miss (unknown / expired / already-claimed / raced) returns one uniform 404 body
    on a uniform response-time floor. Malformed requests are 422. Rate limited per source IP (30/10min)
    and per code (10/10min). NOT exposed as an MCP tool (public credential bootstrap; the MCP surface is
    authenticated).

    Args:
        body (ClaimAgentKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClaimAgentKeyResponse200 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ClaimAgentKeyBody,
) -> ClaimAgentKeyResponse200 | Error | None:
    """Claim a single-use agent API key by claim code

     Public (unauthenticated) claim endpoint for operator-issued agent keys. The customer (or SHC on
    their behalf) mints a key and hands the AGENT only a single-use claim code; the agent exchanges the
    code here exactly once and receives the plaintext key (never recoverable again). Anti-enumeration:
    every existence-type miss (unknown / expired / already-claimed / raced) returns one uniform 404 body
    on a uniform response-time floor. Malformed requests are 422. Rate limited per source IP (30/10min)
    and per code (10/10min). NOT exposed as an MCP tool (public credential bootstrap; the MCP surface is
    authenticated).

    Args:
        body (ClaimAgentKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClaimAgentKeyResponse200 | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
