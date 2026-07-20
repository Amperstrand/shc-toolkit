from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_preferences_update_request import AccountPreferencesUpdateRequest
from ...models.error import Error
from ...models.update_account_preferences_response_200 import (
    UpdateAccountPreferencesResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AccountPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/account/preferences",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UpdateAccountPreferencesResponse200 | None:
    if response.status_code == 200:
        response_200 = UpdateAccountPreferencesResponse200.from_dict(response.json())

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
) -> Response[Error | UpdateAccountPreferencesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AccountPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateAccountPreferencesResponse200]:
    """Update account preferences

     Updates self-scoped, company-editable client preferences (only fields flagged editable; see GET
    /account/preferences `editable`). `autodebit` is not writable through this API. Returns the
    refreshed preferences.

    Args:
        x_user_api_otp (str | Unset):
        body (AccountPreferencesUpdateRequest): Update self-scoped, company-editable client
            preferences. PATCH semantics: only the keys present are changed; at least one field is
            required. Only fields the company has flagged editable (see GET /account/preferences
            `editable`) may be changed. `autodebit` is not writable through this API. Example:
            {'inv_method': 'email', 'receive_email_marketing': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateAccountPreferencesResponse200]
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
    body: AccountPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateAccountPreferencesResponse200 | None:
    """Update account preferences

     Updates self-scoped, company-editable client preferences (only fields flagged editable; see GET
    /account/preferences `editable`). `autodebit` is not writable through this API. Returns the
    refreshed preferences.

    Args:
        x_user_api_otp (str | Unset):
        body (AccountPreferencesUpdateRequest): Update self-scoped, company-editable client
            preferences. PATCH semantics: only the keys present are changed; at least one field is
            required. Only fields the company has flagged editable (see GET /account/preferences
            `editable`) may be changed. `autodebit` is not writable through this API. Example:
            {'inv_method': 'email', 'receive_email_marketing': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateAccountPreferencesResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AccountPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateAccountPreferencesResponse200]:
    """Update account preferences

     Updates self-scoped, company-editable client preferences (only fields flagged editable; see GET
    /account/preferences `editable`). `autodebit` is not writable through this API. Returns the
    refreshed preferences.

    Args:
        x_user_api_otp (str | Unset):
        body (AccountPreferencesUpdateRequest): Update self-scoped, company-editable client
            preferences. PATCH semantics: only the keys present are changed; at least one field is
            required. Only fields the company has flagged editable (see GET /account/preferences
            `editable`) may be changed. `autodebit` is not writable through this API. Example:
            {'inv_method': 'email', 'receive_email_marketing': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateAccountPreferencesResponse200]
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
    body: AccountPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateAccountPreferencesResponse200 | None:
    """Update account preferences

     Updates self-scoped, company-editable client preferences (only fields flagged editable; see GET
    /account/preferences `editable`). `autodebit` is not writable through this API. Returns the
    refreshed preferences.

    Args:
        x_user_api_otp (str | Unset):
        body (AccountPreferencesUpdateRequest): Update self-scoped, company-editable client
            preferences. PATCH semantics: only the keys present are changed; at least one field is
            required. Only fields the company has flagged editable (see GET /account/preferences
            `editable`) may be changed. `autodebit` is not writable through this API. Example:
            {'inv_method': 'email', 'receive_email_marketing': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateAccountPreferencesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
