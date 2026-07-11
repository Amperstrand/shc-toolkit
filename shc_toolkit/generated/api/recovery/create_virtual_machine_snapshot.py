from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_virtual_machine_snapshot_response_202 import (
    CreateVirtualMachineSnapshotResponse202,
)
from ...models.error import Error
from ...models.vm_snapshot_create_request import VmSnapshotCreateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: VmSnapshotCreateRequest | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/snapshots".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateVirtualMachineSnapshotResponse202 | Error | None:
    if response.status_code == 202:
        response_202 = CreateVirtualMachineSnapshotResponse202.from_dict(
            response.json()
        )

        return response_202

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
) -> Response[CreateVirtualMachineSnapshotResponse202 | Error]:
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
    body: VmSnapshotCreateRequest | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CreateVirtualMachineSnapshotResponse202 | Error]:
    """Queue a VM snapshot

     Queues a new snapshot job for one owned VM service. The service must be active, snapshots must be
    enabled for the package, and the snapshot limit must allow another item.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmSnapshotCreateRequest | Unset):  Example: {'name': 'pre-upgrade', 'description':
            'Before major package upgrade'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateVirtualMachineSnapshotResponse202 | Error]
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
    body: VmSnapshotCreateRequest | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> CreateVirtualMachineSnapshotResponse202 | Error | None:
    """Queue a VM snapshot

     Queues a new snapshot job for one owned VM service. The service must be active, snapshots must be
    enabled for the package, and the snapshot limit must allow another item.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmSnapshotCreateRequest | Unset):  Example: {'name': 'pre-upgrade', 'description':
            'Before major package upgrade'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateVirtualMachineSnapshotResponse202 | Error
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
    body: VmSnapshotCreateRequest | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CreateVirtualMachineSnapshotResponse202 | Error]:
    """Queue a VM snapshot

     Queues a new snapshot job for one owned VM service. The service must be active, snapshots must be
    enabled for the package, and the snapshot limit must allow another item.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmSnapshotCreateRequest | Unset):  Example: {'name': 'pre-upgrade', 'description':
            'Before major package upgrade'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateVirtualMachineSnapshotResponse202 | Error]
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
    body: VmSnapshotCreateRequest | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> CreateVirtualMachineSnapshotResponse202 | Error | None:
    """Queue a VM snapshot

     Queues a new snapshot job for one owned VM service. The service must be active, snapshots must be
    enabled for the package, and the snapshot limit must allow another item.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmSnapshotCreateRequest | Unset):  Example: {'name': 'pre-upgrade', 'description':
            'Before major package upgrade'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateVirtualMachineSnapshotResponse202 | Error
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
