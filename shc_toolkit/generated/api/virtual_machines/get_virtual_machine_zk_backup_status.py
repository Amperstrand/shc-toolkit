from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_virtual_machine_zk_backup_status_response_200 import (
    GetVirtualMachineZkBackupStatusResponse200,
)
from ...types import Response


def _get_kwargs(
    service_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/vm/{service_id}/zk-backup/status".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetVirtualMachineZkBackupStatusResponse200 | None:
    if response.status_code == 200:
        response_200 = GetVirtualMachineZkBackupStatusResponse200.from_dict(
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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | GetVirtualMachineZkBackupStatusResponse200]:
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
) -> Response[Error | GetVirtualMachineZkBackupStatusResponse200]:
    """Get VM ZK backup status

     Returns verified ZK backup status for one owned VM. SHC ZK backup is genuine self-custody, the same
    model as Bitcoin: your keys, your data. Backups already sealed to a recovery key stay openable by
    that key until you rotate forward and re-upload the backups you care about; that is the sovereignty
    property. If a recovery key is exposed, register a fresh recipient set and re-upload replacement
    backups, like sweeping a Bitcoin key to a fresh address. SHC cannot re-seal, claw back, or reach
    into existing backup data; that inability is the guarantee.

    Args:
        service_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetVirtualMachineZkBackupStatusResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Error | GetVirtualMachineZkBackupStatusResponse200 | None:
    """Get VM ZK backup status

     Returns verified ZK backup status for one owned VM. SHC ZK backup is genuine self-custody, the same
    model as Bitcoin: your keys, your data. Backups already sealed to a recovery key stay openable by
    that key until you rotate forward and re-upload the backups you care about; that is the sovereignty
    property. If a recovery key is exposed, register a fresh recipient set and re-upload replacement
    backups, like sweeping a Bitcoin key to a fresh address. SHC cannot re-seal, claw back, or reach
    into existing backup data; that inability is the guarantee.

    Args:
        service_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetVirtualMachineZkBackupStatusResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | GetVirtualMachineZkBackupStatusResponse200]:
    """Get VM ZK backup status

     Returns verified ZK backup status for one owned VM. SHC ZK backup is genuine self-custody, the same
    model as Bitcoin: your keys, your data. Backups already sealed to a recovery key stay openable by
    that key until you rotate forward and re-upload the backups you care about; that is the sovereignty
    property. If a recovery key is exposed, register a fresh recipient set and re-upload replacement
    backups, like sweeping a Bitcoin key to a fresh address. SHC cannot re-seal, claw back, or reach
    into existing backup data; that inability is the guarantee.

    Args:
        service_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetVirtualMachineZkBackupStatusResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Error | GetVirtualMachineZkBackupStatusResponse200 | None:
    """Get VM ZK backup status

     Returns verified ZK backup status for one owned VM. SHC ZK backup is genuine self-custody, the same
    model as Bitcoin: your keys, your data. Backups already sealed to a recovery key stay openable by
    that key until you rotate forward and re-upload the backups you care about; that is the sovereignty
    property. If a recovery key is exposed, register a fresh recipient set and re-upload replacement
    backups, like sweeping a Bitcoin key to a fresh address. SHC cannot re-seal, claw back, or reach
    into existing backup data; that inability is the guarantee.

    Args:
        service_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetVirtualMachineZkBackupStatusResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
        )
    ).parsed
