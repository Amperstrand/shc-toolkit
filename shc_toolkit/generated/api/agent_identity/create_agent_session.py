from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_session_create_request import AgentSessionCreateRequest
from ...models.create_agent_session_response_201 import CreateAgentSessionResponse201
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: AgentSessionCreateRequest,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agent-sessions",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateAgentSessionResponse201 | Error | None:
    if response.status_code == 201:
        response_201 = CreateAgentSessionResponse201.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

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
) -> Response[CreateAgentSessionResponse201 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AgentSessionCreateRequest,
    idempotency_key: str,
) -> Response[CreateAgentSessionResponse201 | Error]:
    """Create PoP-bound agent session token

     Mints a customer-owned shc_agent_ bearer token bound to publicKey. Idempotency-Key is required. The
    plaintext token is returned once.

    Args:
        idempotency_key (str):
        body (AgentSessionCreateRequest):  Example: {'agentName': 'invoice-review-agent',
            'agentPurpose': 'Review invoices and open support tickets when approved.', 'publicKey':
            '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', 'scope': 'read'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateAgentSessionResponse201 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: AgentSessionCreateRequest,
    idempotency_key: str,
) -> CreateAgentSessionResponse201 | Error | None:
    """Create PoP-bound agent session token

     Mints a customer-owned shc_agent_ bearer token bound to publicKey. Idempotency-Key is required. The
    plaintext token is returned once.

    Args:
        idempotency_key (str):
        body (AgentSessionCreateRequest):  Example: {'agentName': 'invoice-review-agent',
            'agentPurpose': 'Review invoices and open support tickets when approved.', 'publicKey':
            '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', 'scope': 'read'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateAgentSessionResponse201 | Error
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AgentSessionCreateRequest,
    idempotency_key: str,
) -> Response[CreateAgentSessionResponse201 | Error]:
    """Create PoP-bound agent session token

     Mints a customer-owned shc_agent_ bearer token bound to publicKey. Idempotency-Key is required. The
    plaintext token is returned once.

    Args:
        idempotency_key (str):
        body (AgentSessionCreateRequest):  Example: {'agentName': 'invoice-review-agent',
            'agentPurpose': 'Review invoices and open support tickets when approved.', 'publicKey':
            '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', 'scope': 'read'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateAgentSessionResponse201 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AgentSessionCreateRequest,
    idempotency_key: str,
) -> CreateAgentSessionResponse201 | Error | None:
    """Create PoP-bound agent session token

     Mints a customer-owned shc_agent_ bearer token bound to publicKey. Idempotency-Key is required. The
    plaintext token is returned once.

    Args:
        idempotency_key (str):
        body (AgentSessionCreateRequest):  Example: {'agentName': 'invoice-review-agent',
            'agentPurpose': 'Review invoices and open support tickets when approved.', 'publicKey':
            '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', 'scope': 'read'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateAgentSessionResponse201 | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
