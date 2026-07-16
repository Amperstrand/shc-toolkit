from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.rekey_virtual_machine_zk_backup_response_200 import (
    RekeyVirtualMachineZkBackupResponse200,
)
from ...models.zk_backup_retention_rekey_request import ZkBackupRetentionRekeyRequest
from ...types import Response


def _get_kwargs(
    service_id: int,
    *,
    body: ZkBackupRetentionRekeyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/zk-backup/rekey".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | RekeyVirtualMachineZkBackupResponse200 | None:
    if response.status_code == 200:
        response_200 = RekeyVirtualMachineZkBackupResponse200.from_dict(response.json())

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
) -> Response[Error | RekeyVirtualMachineZkBackupResponse200]:
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
    body: ZkBackupRetentionRekeyRequest,
) -> Response[Error | RekeyVirtualMachineZkBackupResponse200]:
    """Rekey (rotate) a VM's zero-knowledge backup registration

     Rotates the VM ZK backup recipient set forward for future backups while preserving self-custody for
    existing sealed backups. Requires X-User-Api-Confirm and ack=REKEY-WITH-RETENTION with selected
    currently-active recipient fingerprints carried forward into the submitted new set. SHC ZK backup is
    genuine self-custody, the same model as Bitcoin: your keys, your data. Backups already sealed to a
    recovery key stay openable by that key until you rotate forward and re-upload the backups you care
    about; that is the sovereignty property. If a recovery key is exposed, register a fresh recipient
    set and re-upload replacement backups, like sweeping a Bitcoin key to a fresh address. SHC cannot
    re-seal, claw back, or reach into existing backup data; that inability is the guarantee.

    Args:
        service_id (int):
        body (ZkBackupRetentionRekeyRequest): Rotate-forward ZK backup rekey request. Future
            backups use the submitted recipient set; existing backups stay openable by their sealed
            recovery keys until the customer re-uploads the backups they care about.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RekeyVirtualMachineZkBackupResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ZkBackupRetentionRekeyRequest,
) -> Error | RekeyVirtualMachineZkBackupResponse200 | None:
    """Rekey (rotate) a VM's zero-knowledge backup registration

     Rotates the VM ZK backup recipient set forward for future backups while preserving self-custody for
    existing sealed backups. Requires X-User-Api-Confirm and ack=REKEY-WITH-RETENTION with selected
    currently-active recipient fingerprints carried forward into the submitted new set. SHC ZK backup is
    genuine self-custody, the same model as Bitcoin: your keys, your data. Backups already sealed to a
    recovery key stay openable by that key until you rotate forward and re-upload the backups you care
    about; that is the sovereignty property. If a recovery key is exposed, register a fresh recipient
    set and re-upload replacement backups, like sweeping a Bitcoin key to a fresh address. SHC cannot
    re-seal, claw back, or reach into existing backup data; that inability is the guarantee.

    Args:
        service_id (int):
        body (ZkBackupRetentionRekeyRequest): Rotate-forward ZK backup rekey request. Future
            backups use the submitted recipient set; existing backups stay openable by their sealed
            recovery keys until the customer re-uploads the backups they care about.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RekeyVirtualMachineZkBackupResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ZkBackupRetentionRekeyRequest,
) -> Response[Error | RekeyVirtualMachineZkBackupResponse200]:
    """Rekey (rotate) a VM's zero-knowledge backup registration

     Rotates the VM ZK backup recipient set forward for future backups while preserving self-custody for
    existing sealed backups. Requires X-User-Api-Confirm and ack=REKEY-WITH-RETENTION with selected
    currently-active recipient fingerprints carried forward into the submitted new set. SHC ZK backup is
    genuine self-custody, the same model as Bitcoin: your keys, your data. Backups already sealed to a
    recovery key stay openable by that key until you rotate forward and re-upload the backups you care
    about; that is the sovereignty property. If a recovery key is exposed, register a fresh recipient
    set and re-upload replacement backups, like sweeping a Bitcoin key to a fresh address. SHC cannot
    re-seal, claw back, or reach into existing backup data; that inability is the guarantee.

    Args:
        service_id (int):
        body (ZkBackupRetentionRekeyRequest): Rotate-forward ZK backup rekey request. Future
            backups use the submitted recipient set; existing backups stay openable by their sealed
            recovery keys until the customer re-uploads the backups they care about.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RekeyVirtualMachineZkBackupResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ZkBackupRetentionRekeyRequest,
) -> Error | RekeyVirtualMachineZkBackupResponse200 | None:
    """Rekey (rotate) a VM's zero-knowledge backup registration

     Rotates the VM ZK backup recipient set forward for future backups while preserving self-custody for
    existing sealed backups. Requires X-User-Api-Confirm and ack=REKEY-WITH-RETENTION with selected
    currently-active recipient fingerprints carried forward into the submitted new set. SHC ZK backup is
    genuine self-custody, the same model as Bitcoin: your keys, your data. Backups already sealed to a
    recovery key stay openable by that key until you rotate forward and re-upload the backups you care
    about; that is the sovereignty property. If a recovery key is exposed, register a fresh recipient
    set and re-upload replacement backups, like sweeping a Bitcoin key to a fresh address. SHC cannot
    re-seal, claw back, or reach into existing backup data; that inability is the guarantee.

    Args:
        service_id (int):
        body (ZkBackupRetentionRekeyRequest): Rotate-forward ZK backup rekey request. Future
            backups use the submitted recipient set; existing backups stay openable by their sealed
            recovery keys until the customer re-uploads the backups they care about.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RekeyVirtualMachineZkBackupResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
        )
    ).parsed
