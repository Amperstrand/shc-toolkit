from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.preview_virtual_machine_order_response_200 import (
    PreviewVirtualMachineOrderResponse200,
)
from ...models.vm_order_request import VmOrderRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: VmOrderRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/ordering/preview",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | PreviewVirtualMachineOrderResponse200 | None:
    if response.status_code == 200:
        response_200 = PreviewVirtualMachineOrderResponse200.from_dict(response.json())

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
) -> Response[Error | PreviewVirtualMachineOrderResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: VmOrderRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | PreviewVirtualMachineOrderResponse200]:
    """Preview a VM order request

     Validates package selection, billing row, hostname, and optional location choice against the
    authenticated customer's visible storefront scope. This does not create the order or reserve
    capacity.

    Args:
        x_user_api_otp (str | Unset):
        body (VmOrderRequest): Order request for a new VM. Example: {'package_id': 23,
            'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PreviewVirtualMachineOrderResponse200]
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
    client: AuthenticatedClient | Client,
    body: VmOrderRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | PreviewVirtualMachineOrderResponse200 | None:
    """Preview a VM order request

     Validates package selection, billing row, hostname, and optional location choice against the
    authenticated customer's visible storefront scope. This does not create the order or reserve
    capacity.

    Args:
        x_user_api_otp (str | Unset):
        body (VmOrderRequest): Order request for a new VM. Example: {'package_id': 23,
            'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PreviewVirtualMachineOrderResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: VmOrderRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | PreviewVirtualMachineOrderResponse200]:
    """Preview a VM order request

     Validates package selection, billing row, hostname, and optional location choice against the
    authenticated customer's visible storefront scope. This does not create the order or reserve
    capacity.

    Args:
        x_user_api_otp (str | Unset):
        body (VmOrderRequest): Order request for a new VM. Example: {'package_id': 23,
            'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PreviewVirtualMachineOrderResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: VmOrderRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | PreviewVirtualMachineOrderResponse200 | None:
    """Preview a VM order request

     Validates package selection, billing row, hostname, and optional location choice against the
    authenticated customer's visible storefront scope. This does not create the order or reserve
    capacity.

    Args:
        x_user_api_otp (str | Unset):
        body (VmOrderRequest): Order request for a new VM. Example: {'package_id': 23,
            'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PreviewVirtualMachineOrderResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
