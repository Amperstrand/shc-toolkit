from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.update_vm_data_preferences_response_200 import (
    UpdateVmDataPreferencesResponse200,
)
from ...models.vm_data_preferences_update_request import VmDataPreferencesUpdateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: VmDataPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/vm/{service_id}/data-preferences".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UpdateVmDataPreferencesResponse200 | None:
    if response.status_code == 200:
        response_200 = UpdateVmDataPreferencesResponse200.from_dict(response.json())

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
) -> Response[Error | UpdateVmDataPreferencesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmDataPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateVmDataPreferencesResponse200]:
    """Update backup/snapshot data preferences

     Updates backup/snapshot schedule, retention, notification, and encryption-pubkey preferences for one
    owned VM. PATCH semantics: only the sections/keys present are changed. Returns the refreshed
    preferences (same shape as GET). The encryption pubkey value is never returned. If the body contains
    zk_backup for first registration, the request requires X-User-Api-Confirm; SHC writes the initial
    customer recipient set and never receives private key material.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmDataPreferencesUpdateRequest): Update backup/snapshot schedule, retention,
            notification, and encryption-pubkey preferences. PATCH semantics: only the sections/keys
            present are changed. At least one recognized field is expected. If zk_backup is supplied
            for first registration, X-User-Api-Confirm is required before the initial recipient set is
            written. Example: {'backup': {'retention': 'keep-daily=7', 'auto_days': ['mon', 'thu'],
            'auto_time': '03:00'}, 'notify': {'failed': True, 'success': False}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateVmDataPreferencesResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmDataPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateVmDataPreferencesResponse200 | None:
    """Update backup/snapshot data preferences

     Updates backup/snapshot schedule, retention, notification, and encryption-pubkey preferences for one
    owned VM. PATCH semantics: only the sections/keys present are changed. Returns the refreshed
    preferences (same shape as GET). The encryption pubkey value is never returned. If the body contains
    zk_backup for first registration, the request requires X-User-Api-Confirm; SHC writes the initial
    customer recipient set and never receives private key material.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmDataPreferencesUpdateRequest): Update backup/snapshot schedule, retention,
            notification, and encryption-pubkey preferences. PATCH semantics: only the sections/keys
            present are changed. At least one recognized field is expected. If zk_backup is supplied
            for first registration, X-User-Api-Confirm is required before the initial recipient set is
            written. Example: {'backup': {'retention': 'keep-daily=7', 'auto_days': ['mon', 'thu'],
            'auto_time': '03:00'}, 'notify': {'failed': True, 'success': False}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateVmDataPreferencesResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmDataPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateVmDataPreferencesResponse200]:
    """Update backup/snapshot data preferences

     Updates backup/snapshot schedule, retention, notification, and encryption-pubkey preferences for one
    owned VM. PATCH semantics: only the sections/keys present are changed. Returns the refreshed
    preferences (same shape as GET). The encryption pubkey value is never returned. If the body contains
    zk_backup for first registration, the request requires X-User-Api-Confirm; SHC writes the initial
    customer recipient set and never receives private key material.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmDataPreferencesUpdateRequest): Update backup/snapshot schedule, retention,
            notification, and encryption-pubkey preferences. PATCH semantics: only the sections/keys
            present are changed. At least one recognized field is expected. If zk_backup is supplied
            for first registration, X-User-Api-Confirm is required before the initial recipient set is
            written. Example: {'backup': {'retention': 'keep-daily=7', 'auto_days': ['mon', 'thu'],
            'auto_time': '03:00'}, 'notify': {'failed': True, 'success': False}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateVmDataPreferencesResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmDataPreferencesUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateVmDataPreferencesResponse200 | None:
    """Update backup/snapshot data preferences

     Updates backup/snapshot schedule, retention, notification, and encryption-pubkey preferences for one
    owned VM. PATCH semantics: only the sections/keys present are changed. Returns the refreshed
    preferences (same shape as GET). The encryption pubkey value is never returned. If the body contains
    zk_backup for first registration, the request requires X-User-Api-Confirm; SHC writes the initial
    customer recipient set and never receives private key material.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmDataPreferencesUpdateRequest): Update backup/snapshot schedule, retention,
            notification, and encryption-pubkey preferences. PATCH semantics: only the sections/keys
            present are changed. At least one recognized field is expected. If zk_backup is supplied
            for first registration, X-User-Api-Confirm is required before the initial recipient set is
            written. Example: {'backup': {'retention': 'keep-daily=7', 'auto_days': ['mon', 'thu'],
            'auto_time': '03:00'}, 'notify': {'failed': True, 'success': False}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateVmDataPreferencesResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
