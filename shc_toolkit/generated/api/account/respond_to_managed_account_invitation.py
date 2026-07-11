from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.managed_account_invitation_request import ManagedAccountInvitationRequest
from ...models.respond_to_managed_account_invitation_response_200 import (
    RespondToManagedAccountInvitationResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    token: str,
    *,
    body: ManagedAccountInvitationRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-accounts/invitations/{token}".format(
            token=quote(str(token), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | RespondToManagedAccountInvitationResponse200 | None:
    if response.status_code == 200:
        response_200 = RespondToManagedAccountInvitationResponse200.from_dict(
            response.json()
        )

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

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
) -> Response[Error | RespondToManagedAccountInvitationResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token: str,
    *,
    client: AuthenticatedClient,
    body: ManagedAccountInvitationRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | RespondToManagedAccountInvitationResponse200]:
    """Accept or decline a management invitation

     Accepts or declines an account-management invitation addressed to the authenticated client. 404
    existence-hiding for invalid tokens, email mismatches, cross-company, or self-issued invitations.
    Accepting an already-accepted invitation is idempotent (200).

    Args:
        token (str):
        x_user_api_otp (str | Unset):
        body (ManagedAccountInvitationRequest): Accept or decline a management invitation
            addressed to the authenticated client. Example: {'action': 'accept'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RespondToManagedAccountInvitationResponse200]
    """

    kwargs = _get_kwargs(
        token=token,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    token: str,
    *,
    client: AuthenticatedClient,
    body: ManagedAccountInvitationRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | RespondToManagedAccountInvitationResponse200 | None:
    """Accept or decline a management invitation

     Accepts or declines an account-management invitation addressed to the authenticated client. 404
    existence-hiding for invalid tokens, email mismatches, cross-company, or self-issued invitations.
    Accepting an already-accepted invitation is idempotent (200).

    Args:
        token (str):
        x_user_api_otp (str | Unset):
        body (ManagedAccountInvitationRequest): Accept or decline a management invitation
            addressed to the authenticated client. Example: {'action': 'accept'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RespondToManagedAccountInvitationResponse200
    """

    return sync_detailed(
        token=token,
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    token: str,
    *,
    client: AuthenticatedClient,
    body: ManagedAccountInvitationRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | RespondToManagedAccountInvitationResponse200]:
    """Accept or decline a management invitation

     Accepts or declines an account-management invitation addressed to the authenticated client. 404
    existence-hiding for invalid tokens, email mismatches, cross-company, or self-issued invitations.
    Accepting an already-accepted invitation is idempotent (200).

    Args:
        token (str):
        x_user_api_otp (str | Unset):
        body (ManagedAccountInvitationRequest): Accept or decline a management invitation
            addressed to the authenticated client. Example: {'action': 'accept'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RespondToManagedAccountInvitationResponse200]
    """

    kwargs = _get_kwargs(
        token=token,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    token: str,
    *,
    client: AuthenticatedClient,
    body: ManagedAccountInvitationRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | RespondToManagedAccountInvitationResponse200 | None:
    """Accept or decline a management invitation

     Accepts or declines an account-management invitation addressed to the authenticated client. 404
    existence-hiding for invalid tokens, email mismatches, cross-company, or self-issued invitations.
    Accepting an already-accepted invitation is idempotent (200).

    Args:
        token (str):
        x_user_api_otp (str | Unset):
        body (ManagedAccountInvitationRequest): Accept or decline a management invitation
            addressed to the authenticated client. Example: {'action': 'accept'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RespondToManagedAccountInvitationResponse200
    """

    return (
        await asyncio_detailed(
            token=token,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
