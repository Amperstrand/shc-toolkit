from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.reply_support_ticket_response_201 import ReplySupportTicketResponse201
from ...models.support_ticket_reply_request import SupportTicketReplyRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    ticket_id: int,
    *,
    body: SupportTicketReplyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/support/tickets/{ticket_id}/replies".format(
            ticket_id=quote(str(ticket_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ReplySupportTicketResponse201 | None:
    if response.status_code == 201:
        response_201 = ReplySupportTicketResponse201.from_dict(response.json())

        return response_201

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
) -> Response[Error | ReplySupportTicketResponse201]:
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
    body: SupportTicketReplyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ReplySupportTicketResponse201]:
    """Reply to a support ticket

     Adds a reply to an owned ticket (404 existence-hiding for foreign/missing tickets). Replying to a
    closed/awaiting-reply ticket reopens it. Supports base64 attachments.

    Args:
        ticket_id (int):  Example: 501.
        x_user_api_otp (str | Unset):
        body (SupportTicketReplyRequest): Add a reply to an owned ticket. Replying to a
            closed/awaiting-reply ticket reopens it. Example: {'message': 'Still happening after a
            reboot.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ReplySupportTicketResponse201]
    """

    kwargs = _get_kwargs(
        ticket_id=ticket_id,
        body=body,
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
    body: SupportTicketReplyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ReplySupportTicketResponse201 | None:
    """Reply to a support ticket

     Adds a reply to an owned ticket (404 existence-hiding for foreign/missing tickets). Replying to a
    closed/awaiting-reply ticket reopens it. Supports base64 attachments.

    Args:
        ticket_id (int):  Example: 501.
        x_user_api_otp (str | Unset):
        body (SupportTicketReplyRequest): Add a reply to an owned ticket. Replying to a
            closed/awaiting-reply ticket reopens it. Example: {'message': 'Still happening after a
            reboot.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ReplySupportTicketResponse201
    """

    return sync_detailed(
        ticket_id=ticket_id,
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    body: SupportTicketReplyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ReplySupportTicketResponse201]:
    """Reply to a support ticket

     Adds a reply to an owned ticket (404 existence-hiding for foreign/missing tickets). Replying to a
    closed/awaiting-reply ticket reopens it. Supports base64 attachments.

    Args:
        ticket_id (int):  Example: 501.
        x_user_api_otp (str | Unset):
        body (SupportTicketReplyRequest): Add a reply to an owned ticket. Replying to a
            closed/awaiting-reply ticket reopens it. Example: {'message': 'Still happening after a
            reboot.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ReplySupportTicketResponse201]
    """

    kwargs = _get_kwargs(
        ticket_id=ticket_id,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    body: SupportTicketReplyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ReplySupportTicketResponse201 | None:
    """Reply to a support ticket

     Adds a reply to an owned ticket (404 existence-hiding for foreign/missing tickets). Replying to a
    closed/awaiting-reply ticket reopens it. Supports base64 attachments.

    Args:
        ticket_id (int):  Example: 501.
        x_user_api_otp (str | Unset):
        body (SupportTicketReplyRequest): Add a reply to an owned ticket. Replying to a
            closed/awaiting-reply ticket reopens it. Example: {'message': 'Still happening after a
            reboot.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ReplySupportTicketResponse201
    """

    return (
        await asyncio_detailed(
            ticket_id=ticket_id,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
