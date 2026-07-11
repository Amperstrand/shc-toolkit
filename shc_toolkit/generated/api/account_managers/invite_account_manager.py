from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.invite_account_manager_response_201 import (
    InviteAccountManagerResponse201,
)
from ...models.manager_invite_request import ManagerInviteRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ManagerInviteRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managers",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | InviteAccountManagerResponse201 | None:
    if response.status_code == 201:
        response_201 = InviteAccountManagerResponse201.from_dict(response.json())

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
) -> Response[Error | InviteAccountManagerResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ManagerInviteRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | InviteAccountManagerResponse201]:
    """Invite an account manager

     Invites a person (by email) to manage the authenticated customer's account, granting the supplied
    permission areas (parity with the portal add-manager flow). `permissions` is a non-empty array of
    area keys from GET /managers/permission-options (the contact vocabulary minus `_managed`). The email
    must be the primary contact of an existing account in the same company; if it is not, the invitation
    is recorded with status `invalid` and no email is sent (stock Blesta behavior). A second pending
    invitation for the same email returns 409.

    Args:
        x_user_api_otp (str | Unset):
        body (ManagerInviteRequest): Fields for inviting an account manager. Mirrors the portal
            add-manager form. Example: {'email': 'manager@example.com', 'permissions':
            ['client_invoices', 'client_services']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | InviteAccountManagerResponse201]
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
    body: ManagerInviteRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | InviteAccountManagerResponse201 | None:
    """Invite an account manager

     Invites a person (by email) to manage the authenticated customer's account, granting the supplied
    permission areas (parity with the portal add-manager flow). `permissions` is a non-empty array of
    area keys from GET /managers/permission-options (the contact vocabulary minus `_managed`). The email
    must be the primary contact of an existing account in the same company; if it is not, the invitation
    is recorded with status `invalid` and no email is sent (stock Blesta behavior). A second pending
    invitation for the same email returns 409.

    Args:
        x_user_api_otp (str | Unset):
        body (ManagerInviteRequest): Fields for inviting an account manager. Mirrors the portal
            add-manager form. Example: {'email': 'manager@example.com', 'permissions':
            ['client_invoices', 'client_services']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | InviteAccountManagerResponse201
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ManagerInviteRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | InviteAccountManagerResponse201]:
    """Invite an account manager

     Invites a person (by email) to manage the authenticated customer's account, granting the supplied
    permission areas (parity with the portal add-manager flow). `permissions` is a non-empty array of
    area keys from GET /managers/permission-options (the contact vocabulary minus `_managed`). The email
    must be the primary contact of an existing account in the same company; if it is not, the invitation
    is recorded with status `invalid` and no email is sent (stock Blesta behavior). A second pending
    invitation for the same email returns 409.

    Args:
        x_user_api_otp (str | Unset):
        body (ManagerInviteRequest): Fields for inviting an account manager. Mirrors the portal
            add-manager form. Example: {'email': 'manager@example.com', 'permissions':
            ['client_invoices', 'client_services']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | InviteAccountManagerResponse201]
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
    body: ManagerInviteRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | InviteAccountManagerResponse201 | None:
    """Invite an account manager

     Invites a person (by email) to manage the authenticated customer's account, granting the supplied
    permission areas (parity with the portal add-manager flow). `permissions` is a non-empty array of
    area keys from GET /managers/permission-options (the contact vocabulary minus `_managed`). The email
    must be the primary contact of an existing account in the same company; if it is not, the invitation
    is recorded with status `invalid` and no email is sent (stock Blesta behavior). A second pending
    invitation for the same email returns 409.

    Args:
        x_user_api_otp (str | Unset):
        body (ManagerInviteRequest): Fields for inviting an account manager. Mirrors the portal
            add-manager form. Example: {'email': 'manager@example.com', 'permissions':
            ['client_invoices', 'client_services']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | InviteAccountManagerResponse201
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
