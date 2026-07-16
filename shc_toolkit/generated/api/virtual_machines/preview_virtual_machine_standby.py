from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.preview_virtual_machine_standby_response_200 import (
    PreviewVirtualMachineStandbyResponse200,
)
from ...types import Response


def _get_kwargs(
    service_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/vm/{service_id}/standby/preview".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | PreviewVirtualMachineStandbyResponse200 | None:
    if response.status_code == 200:
        response_200 = PreviewVirtualMachineStandbyResponse200.from_dict(
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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | PreviewVirtualMachineStandbyResponse200]:
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
) -> Response[Error | PreviewVirtualMachineStandbyResponse200]:
    """Preview standby pricing for a VM

     Read-only quote for parking an authenticated-client-owned VM. Returns both keep-IP and release-IP
    recurring standby price and park credit, plus the keep-IP recurring delta. This returns the standby
    quote and does not confirm, reserve idempotency, stop the VM, change billing, or touch IPs.

    Args:
        service_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PreviewVirtualMachineStandbyResponse200]
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
) -> Error | PreviewVirtualMachineStandbyResponse200 | None:
    """Preview standby pricing for a VM

     Read-only quote for parking an authenticated-client-owned VM. Returns both keep-IP and release-IP
    recurring standby price and park credit, plus the keep-IP recurring delta. This returns the standby
    quote and does not confirm, reserve idempotency, stop the VM, change billing, or touch IPs.

    Args:
        service_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PreviewVirtualMachineStandbyResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | PreviewVirtualMachineStandbyResponse200]:
    """Preview standby pricing for a VM

     Read-only quote for parking an authenticated-client-owned VM. Returns both keep-IP and release-IP
    recurring standby price and park credit, plus the keep-IP recurring delta. This returns the standby
    quote and does not confirm, reserve idempotency, stop the VM, change billing, or touch IPs.

    Args:
        service_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PreviewVirtualMachineStandbyResponse200]
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
) -> Error | PreviewVirtualMachineStandbyResponse200 | None:
    """Preview standby pricing for a VM

     Read-only quote for parking an authenticated-client-owned VM. Returns both keep-IP and release-IP
    recurring standby price and park credit, plus the keep-IP recurring delta. This returns the standby
    quote and does not confirm, reserve idempotency, stop the VM, change billing, or touch IPs.

    Args:
        service_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PreviewVirtualMachineStandbyResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
        )
    ).parsed
