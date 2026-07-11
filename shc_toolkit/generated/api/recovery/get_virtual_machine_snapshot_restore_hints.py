from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_virtual_machine_snapshot_restore_hints_response_200 import (
    GetVirtualMachineSnapshotRestoreHintsResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    backup_id: str,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["backup_id"] = backup_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/vm/{service_id}/snapshots/restore-hints".format(
            service_id=quote(str(service_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetVirtualMachineSnapshotRestoreHintsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetVirtualMachineSnapshotRestoreHintsResponse200.from_dict(
            response.json()
        )

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())

        return response_502

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | GetVirtualMachineSnapshotRestoreHintsResponse200]:
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
    backup_id: str,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetVirtualMachineSnapshotRestoreHintsResponse200]:
    """Check snapshot restore-point encryption status

     Reports whether a snapshot restore point on one owned VM service is encrypted. Client-side backup
    encryption is not yet available, so this currently always reports encrypted:false (no encrypted
    restore points exist).

    Args:
        service_id (int):
        backup_id (str):  Example: bk_6ERwSd_PLY66FW72VFM.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetVirtualMachineSnapshotRestoreHintsResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        backup_id=backup_id,
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
    backup_id: str,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetVirtualMachineSnapshotRestoreHintsResponse200 | None:
    """Check snapshot restore-point encryption status

     Reports whether a snapshot restore point on one owned VM service is encrypted. Client-side backup
    encryption is not yet available, so this currently always reports encrypted:false (no encrypted
    restore points exist).

    Args:
        service_id (int):
        backup_id (str):  Example: bk_6ERwSd_PLY66FW72VFM.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetVirtualMachineSnapshotRestoreHintsResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        backup_id=backup_id,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    backup_id: str,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetVirtualMachineSnapshotRestoreHintsResponse200]:
    """Check snapshot restore-point encryption status

     Reports whether a snapshot restore point on one owned VM service is encrypted. Client-side backup
    encryption is not yet available, so this currently always reports encrypted:false (no encrypted
    restore points exist).

    Args:
        service_id (int):
        backup_id (str):  Example: bk_6ERwSd_PLY66FW72VFM.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetVirtualMachineSnapshotRestoreHintsResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        backup_id=backup_id,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    backup_id: str,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetVirtualMachineSnapshotRestoreHintsResponse200 | None:
    """Check snapshot restore-point encryption status

     Reports whether a snapshot restore point on one owned VM service is encrypted. Client-side backup
    encryption is not yet available, so this currently always reports encrypted:false (no encrypted
    restore points exist).

    Args:
        service_id (int):
        backup_id (str):  Example: bk_6ERwSd_PLY66FW72VFM.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetVirtualMachineSnapshotRestoreHintsResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            backup_id=backup_id,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
