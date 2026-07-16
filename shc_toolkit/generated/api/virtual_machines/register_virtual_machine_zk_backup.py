from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.register_virtual_machine_zk_backup_response_201 import (
    RegisterVirtualMachineZkBackupResponse201,
)
from ...models.zk_backup_registration import ZkBackupRegistration
from ...types import Response


def _get_kwargs(
    service_id: int,
    *,
    body: ZkBackupRegistration,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/zk-backup/register".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | RegisterVirtualMachineZkBackupResponse201 | None:
    if response.status_code == 201:
        response_201 = RegisterVirtualMachineZkBackupResponse201.from_dict(
            response.json()
        )

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
) -> Response[Error | RegisterVirtualMachineZkBackupResponse201]:
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
    body: ZkBackupRegistration,
) -> Response[Error | RegisterVirtualMachineZkBackupResponse201]:
    """Register a VM ZK backup recipient set

     Registers the initial customer-controlled ZK backup config and full recipient set. Requires X-User-
    Api-Confirm. SHC receives only public recipient material and KDF parameters, never private keys or
    passphrases. This starts the customer's self-custody recipient set; use rotate-forward rekey for
    future recipient changes.

    Args:
        service_id (int):
        body (ZkBackupRegistration): Zero-knowledge backup registration: client-derived X25519
            pubkeys + immutable KDF config. Exactly one recipient must be kind=password (the primary).
            The server never sees the password or private keys. Example: {'config': {'v': 1, 'alg':
            'argon2id13', 'ctx': 'shc-vps-backup-v1', 'ops': 3, 'mem': 268435456, 'salt':
            '0f1e2d3c4b5a69788796a5b4c3d2e1f0'}, 'recipients': [{'kind': 'password', 'pubkey':
            'b3c1e4a7d20f5986cc417b0e2d9a6f3418e7c05b9a2d1f6034785c6b9e0a1d2f', 'label': 'primary'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RegisterVirtualMachineZkBackupResponse201]
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
    body: ZkBackupRegistration,
) -> Error | RegisterVirtualMachineZkBackupResponse201 | None:
    """Register a VM ZK backup recipient set

     Registers the initial customer-controlled ZK backup config and full recipient set. Requires X-User-
    Api-Confirm. SHC receives only public recipient material and KDF parameters, never private keys or
    passphrases. This starts the customer's self-custody recipient set; use rotate-forward rekey for
    future recipient changes.

    Args:
        service_id (int):
        body (ZkBackupRegistration): Zero-knowledge backup registration: client-derived X25519
            pubkeys + immutable KDF config. Exactly one recipient must be kind=password (the primary).
            The server never sees the password or private keys. Example: {'config': {'v': 1, 'alg':
            'argon2id13', 'ctx': 'shc-vps-backup-v1', 'ops': 3, 'mem': 268435456, 'salt':
            '0f1e2d3c4b5a69788796a5b4c3d2e1f0'}, 'recipients': [{'kind': 'password', 'pubkey':
            'b3c1e4a7d20f5986cc417b0e2d9a6f3418e7c05b9a2d1f6034785c6b9e0a1d2f', 'label': 'primary'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RegisterVirtualMachineZkBackupResponse201
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
    body: ZkBackupRegistration,
) -> Response[Error | RegisterVirtualMachineZkBackupResponse201]:
    """Register a VM ZK backup recipient set

     Registers the initial customer-controlled ZK backup config and full recipient set. Requires X-User-
    Api-Confirm. SHC receives only public recipient material and KDF parameters, never private keys or
    passphrases. This starts the customer's self-custody recipient set; use rotate-forward rekey for
    future recipient changes.

    Args:
        service_id (int):
        body (ZkBackupRegistration): Zero-knowledge backup registration: client-derived X25519
            pubkeys + immutable KDF config. Exactly one recipient must be kind=password (the primary).
            The server never sees the password or private keys. Example: {'config': {'v': 1, 'alg':
            'argon2id13', 'ctx': 'shc-vps-backup-v1', 'ops': 3, 'mem': 268435456, 'salt':
            '0f1e2d3c4b5a69788796a5b4c3d2e1f0'}, 'recipients': [{'kind': 'password', 'pubkey':
            'b3c1e4a7d20f5986cc417b0e2d9a6f3418e7c05b9a2d1f6034785c6b9e0a1d2f', 'label': 'primary'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RegisterVirtualMachineZkBackupResponse201]
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
    body: ZkBackupRegistration,
) -> Error | RegisterVirtualMachineZkBackupResponse201 | None:
    """Register a VM ZK backup recipient set

     Registers the initial customer-controlled ZK backup config and full recipient set. Requires X-User-
    Api-Confirm. SHC receives only public recipient material and KDF parameters, never private keys or
    passphrases. This starts the customer's self-custody recipient set; use rotate-forward rekey for
    future recipient changes.

    Args:
        service_id (int):
        body (ZkBackupRegistration): Zero-knowledge backup registration: client-derived X25519
            pubkeys + immutable KDF config. Exactly one recipient must be kind=password (the primary).
            The server never sees the password or private keys. Example: {'config': {'v': 1, 'alg':
            'argon2id13', 'ctx': 'shc-vps-backup-v1', 'ops': 3, 'mem': 268435456, 'salt':
            '0f1e2d3c4b5a69788796a5b4c3d2e1f0'}, 'recipients': [{'kind': 'password', 'pubkey':
            'b3c1e4a7d20f5986cc417b0e2d9a6f3418e7c05b9a2d1f6034785c6b9e0a1d2f', 'label': 'primary'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RegisterVirtualMachineZkBackupResponse201
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
        )
    ).parsed
