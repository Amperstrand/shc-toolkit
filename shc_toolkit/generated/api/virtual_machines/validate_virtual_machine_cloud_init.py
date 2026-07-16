from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cloud_init_request import CloudInitRequest
from ...models.error import Error
from ...models.problem import Problem
from ...models.validate_virtual_machine_cloud_init_response_200 import (
    ValidateVirtualMachineCloudInitResponse200,
)
from ...types import Response


def _get_kwargs(
    virtual_machine_id: int,
    *,
    body: CloudInitRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/virtual-machines/{virtual_machine_id}/cloud-init/validate".format(
            virtual_machine_id=quote(str(virtual_machine_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | Problem | ValidateVirtualMachineCloudInitResponse200 | None:
    if response.status_code == 200:
        response_200 = ValidateVirtualMachineCloudInitResponse200.from_dict(
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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

    if response.status_code == 422:
        response_422 = Problem.from_dict(response.json())

        return response_422

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
) -> Response[Error | Problem | ValidateVirtualMachineCloudInitResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    virtual_machine_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CloudInitRequest,
) -> Response[Error | Problem | ValidateVirtualMachineCloudInitResponse200]:
    r"""Validate VM cloud-init user-data

     No-commit security lint for customer-supplied #cloud-config content. The operation accepts content
    only, derives node/storage/ISO identity server-side, and commits nothing.

    Args:
        virtual_machine_id (int):
        body (CloudInitRequest):  Example: {'cloudInit': '#cloud-config\npackage_update: true\n'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Problem | ValidateVirtualMachineCloudInitResponse200]
    """

    kwargs = _get_kwargs(
        virtual_machine_id=virtual_machine_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    virtual_machine_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CloudInitRequest,
) -> Error | Problem | ValidateVirtualMachineCloudInitResponse200 | None:
    r"""Validate VM cloud-init user-data

     No-commit security lint for customer-supplied #cloud-config content. The operation accepts content
    only, derives node/storage/ISO identity server-side, and commits nothing.

    Args:
        virtual_machine_id (int):
        body (CloudInitRequest):  Example: {'cloudInit': '#cloud-config\npackage_update: true\n'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Problem | ValidateVirtualMachineCloudInitResponse200
    """

    return sync_detailed(
        virtual_machine_id=virtual_machine_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    virtual_machine_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CloudInitRequest,
) -> Response[Error | Problem | ValidateVirtualMachineCloudInitResponse200]:
    r"""Validate VM cloud-init user-data

     No-commit security lint for customer-supplied #cloud-config content. The operation accepts content
    only, derives node/storage/ISO identity server-side, and commits nothing.

    Args:
        virtual_machine_id (int):
        body (CloudInitRequest):  Example: {'cloudInit': '#cloud-config\npackage_update: true\n'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Problem | ValidateVirtualMachineCloudInitResponse200]
    """

    kwargs = _get_kwargs(
        virtual_machine_id=virtual_machine_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    virtual_machine_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CloudInitRequest,
) -> Error | Problem | ValidateVirtualMachineCloudInitResponse200 | None:
    r"""Validate VM cloud-init user-data

     No-commit security lint for customer-supplied #cloud-config content. The operation accepts content
    only, derives node/storage/ISO identity server-side, and commits nothing.

    Args:
        virtual_machine_id (int):
        body (CloudInitRequest):  Example: {'cloudInit': '#cloud-config\npackage_update: true\n'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Problem | ValidateVirtualMachineCloudInitResponse200
    """

    return (
        await asyncio_detailed(
            virtual_machine_id=virtual_machine_id,
            client=client,
            body=body,
        )
    ).parsed
