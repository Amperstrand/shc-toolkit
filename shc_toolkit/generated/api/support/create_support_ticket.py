from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_support_ticket_response_201 import CreateSupportTicketResponse201
from ...models.error import Error
from ...models.support_ticket_create_request import SupportTicketCreateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: SupportTicketCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/support/tickets",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateSupportTicketResponse201 | Error | None:
    if response.status_code == 201:
        response_201 = CreateSupportTicketResponse201.from_dict(response.json())

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
) -> Response[CreateSupportTicketResponse201 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SupportTicketCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CreateSupportTicketResponse201 | Error]:
    """Create a support ticket

     Opens a support ticket in a department visible to the authenticated client. Supports base64-encoded
    attachments (subject to a total-size cap).

    Args:
        x_user_api_otp (str | Unset):
        body (SupportTicketCreateRequest): Create a support ticket. `department_id`, `subject`,
            and `message` are required. Example: {'department_id': 1, 'subject': 'Cannot reach my VM
            over SSH', 'message': 'My VM stopped responding to SSH around 14:00 UTC.', 'priority':
            'medium'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateSupportTicketResponse201 | Error]
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
    body: SupportTicketCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> CreateSupportTicketResponse201 | Error | None:
    """Create a support ticket

     Opens a support ticket in a department visible to the authenticated client. Supports base64-encoded
    attachments (subject to a total-size cap).

    Args:
        x_user_api_otp (str | Unset):
        body (SupportTicketCreateRequest): Create a support ticket. `department_id`, `subject`,
            and `message` are required. Example: {'department_id': 1, 'subject': 'Cannot reach my VM
            over SSH', 'message': 'My VM stopped responding to SSH around 14:00 UTC.', 'priority':
            'medium'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateSupportTicketResponse201 | Error
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SupportTicketCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CreateSupportTicketResponse201 | Error]:
    """Create a support ticket

     Opens a support ticket in a department visible to the authenticated client. Supports base64-encoded
    attachments (subject to a total-size cap).

    Args:
        x_user_api_otp (str | Unset):
        body (SupportTicketCreateRequest): Create a support ticket. `department_id`, `subject`,
            and `message` are required. Example: {'department_id': 1, 'subject': 'Cannot reach my VM
            over SSH', 'message': 'My VM stopped responding to SSH around 14:00 UTC.', 'priority':
            'medium'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateSupportTicketResponse201 | Error]
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
    body: SupportTicketCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> CreateSupportTicketResponse201 | Error | None:
    """Create a support ticket

     Opens a support ticket in a department visible to the authenticated client. Supports base64-encoded
    attachments (subject to a total-size cap).

    Args:
        x_user_api_otp (str | Unset):
        body (SupportTicketCreateRequest): Create a support ticket. `department_id`, `subject`,
            and `message` are required. Example: {'department_id': 1, 'subject': 'Cannot reach my VM
            over SSH', 'message': 'My VM stopped responding to SSH around 14:00 UTC.', 'priority':
            'medium'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateSupportTicketResponse201 | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
