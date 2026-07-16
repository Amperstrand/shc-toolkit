from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.submit_support_ticket_feedback_body import (
    SubmitSupportTicketFeedbackBody,
)
from ...models.submit_support_ticket_feedback_response_200 import (
    SubmitSupportTicketFeedbackResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    ticket_id: int,
    *,
    body: SubmitSupportTicketFeedbackBody,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/support/tickets/{ticket_id}/feedback".format(
            ticket_id=quote(str(ticket_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | SubmitSupportTicketFeedbackResponse200 | None:
    if response.status_code == 200:
        response_200 = SubmitSupportTicketFeedbackResponse200.from_dict(response.json())

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | SubmitSupportTicketFeedbackResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ticket_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: SubmitSupportTicketFeedbackBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SubmitSupportTicketFeedbackResponse200]:
    """Record feedback for an owned support ticket

     Submit or replace feedback for an authenticated-client-owned closed support ticket.

    Args:
        ticket_id (int):
        x_user_api_otp (str | Unset):
        body (SubmitSupportTicketFeedbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SubmitSupportTicketFeedbackResponse200]
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
    client: AuthenticatedClient | Client,
    body: SubmitSupportTicketFeedbackBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SubmitSupportTicketFeedbackResponse200 | None:
    """Record feedback for an owned support ticket

     Submit or replace feedback for an authenticated-client-owned closed support ticket.

    Args:
        ticket_id (int):
        x_user_api_otp (str | Unset):
        body (SubmitSupportTicketFeedbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SubmitSupportTicketFeedbackResponse200
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
    client: AuthenticatedClient | Client,
    body: SubmitSupportTicketFeedbackBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SubmitSupportTicketFeedbackResponse200]:
    """Record feedback for an owned support ticket

     Submit or replace feedback for an authenticated-client-owned closed support ticket.

    Args:
        ticket_id (int):
        x_user_api_otp (str | Unset):
        body (SubmitSupportTicketFeedbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SubmitSupportTicketFeedbackResponse200]
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
    client: AuthenticatedClient | Client,
    body: SubmitSupportTicketFeedbackBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SubmitSupportTicketFeedbackResponse200 | None:
    """Record feedback for an owned support ticket

     Submit or replace feedback for an authenticated-client-owned closed support ticket.

    Args:
        ticket_id (int):
        x_user_api_otp (str | Unset):
        body (SubmitSupportTicketFeedbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SubmitSupportTicketFeedbackResponse200
    """

    return (
        await asyncio_detailed(
            ticket_id=ticket_id,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
