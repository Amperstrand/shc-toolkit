from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.revoke_agent_session_response_200 import RevokeAgentSessionResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    session_id: str,
    *,
    x_user_api_confirm: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_confirm, Unset):
        headers["X-User-Api-Confirm"] = x_user_api_confirm

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/agent-sessions/{session_id}".format(
            session_id=quote(str(session_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | RevokeAgentSessionResponse200 | None:
    if response.status_code == 200:
        response_200 = RevokeAgentSessionResponse200.from_dict(response.json())

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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 405:
        response_405 = Error.from_dict(response.json())

        return response_405

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

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
) -> Response[Error | RevokeAgentSessionResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    *,
    client: AuthenticatedClient,
    x_user_api_confirm: str | Unset = UNSET,
) -> Response[Error | RevokeAgentSessionResponse200]:
    """Revoke agent session

     Confirm-gated revocation for a customer-owned agent session. A request without a valid X-User-Api-
    Confirm challenge returns 409 and does not revoke.

    Args:
        session_id (str):
        x_user_api_confirm (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RevokeAgentSessionResponse200]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        x_user_api_confirm=x_user_api_confirm,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    *,
    client: AuthenticatedClient,
    x_user_api_confirm: str | Unset = UNSET,
) -> Error | RevokeAgentSessionResponse200 | None:
    """Revoke agent session

     Confirm-gated revocation for a customer-owned agent session. A request without a valid X-User-Api-
    Confirm challenge returns 409 and does not revoke.

    Args:
        session_id (str):
        x_user_api_confirm (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RevokeAgentSessionResponse200
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        x_user_api_confirm=x_user_api_confirm,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: AuthenticatedClient,
    x_user_api_confirm: str | Unset = UNSET,
) -> Response[Error | RevokeAgentSessionResponse200]:
    """Revoke agent session

     Confirm-gated revocation for a customer-owned agent session. A request without a valid X-User-Api-
    Confirm challenge returns 409 and does not revoke.

    Args:
        session_id (str):
        x_user_api_confirm (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RevokeAgentSessionResponse200]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        x_user_api_confirm=x_user_api_confirm,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: AuthenticatedClient,
    x_user_api_confirm: str | Unset = UNSET,
) -> Error | RevokeAgentSessionResponse200 | None:
    """Revoke agent session

     Confirm-gated revocation for a customer-owned agent session. A request without a valid X-User-Api-
    Confirm challenge returns 409 and does not revoke.

    Args:
        session_id (str):
        x_user_api_confirm (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RevokeAgentSessionResponse200
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            x_user_api_confirm=x_user_api_confirm,
        )
    ).parsed
