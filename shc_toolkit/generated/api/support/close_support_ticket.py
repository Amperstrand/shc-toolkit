from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.close_support_ticket_response_200 import CloseSupportTicketResponse200
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    ticket_id: int,
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
        "method": "post",
        "url": "/support/tickets/{ticket_id}/close".format(
            ticket_id=quote(str(ticket_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CloseSupportTicketResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = CloseSupportTicketResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

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
) -> Response[CloseSupportTicketResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CloseSupportTicketResponse200 | Error]:
    """Close a support ticket

     Closes an owned ticket (404 existence-hiding for foreign/missing). Idempotent: closing an already-
    closed ticket returns 200. The request body is optional; if present it must be an empty JSON object
    (any field is rejected).

    Args:
        ticket_id (int):  Example: 501.
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloseSupportTicketResponse200 | Error]
    """

    kwargs = _get_kwargs(
        ticket_id=ticket_id,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> CloseSupportTicketResponse200 | Error | None:
    """Close a support ticket

     Closes an owned ticket (404 existence-hiding for foreign/missing). Idempotent: closing an already-
    closed ticket returns 200. The request body is optional; if present it must be an empty JSON object
    (any field is rejected).

    Args:
        ticket_id (int):  Example: 501.
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloseSupportTicketResponse200 | Error
    """

    return sync_detailed(
        ticket_id=ticket_id,
        client=client,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CloseSupportTicketResponse200 | Error]:
    """Close a support ticket

     Closes an owned ticket (404 existence-hiding for foreign/missing). Idempotent: closing an already-
    closed ticket returns 200. The request body is optional; if present it must be an empty JSON object
    (any field is rejected).

    Args:
        ticket_id (int):  Example: 501.
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CloseSupportTicketResponse200 | Error]
    """

    kwargs = _get_kwargs(
        ticket_id=ticket_id,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> CloseSupportTicketResponse200 | Error | None:
    """Close a support ticket

     Closes an owned ticket (404 existence-hiding for foreign/missing). Idempotent: closing an already-
    closed ticket returns 200. The request body is optional; if present it must be an empty JSON object
    (any field is rejected).

    Args:
        ticket_id (int):  Example: 501.
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CloseSupportTicketResponse200 | Error
    """

    return (
        await asyncio_detailed(
            ticket_id=ticket_id,
            client=client,
            confirm=confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
