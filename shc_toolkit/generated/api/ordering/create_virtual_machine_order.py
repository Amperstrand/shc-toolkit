from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_virtual_machine_order_response_201 import (
    CreateVirtualMachineOrderResponse201,
)
from ...models.error import Error
from ...models.vm_order_request import VmOrderRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: VmOrderRequest,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/ordering/submit",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateVirtualMachineOrderResponse201 | Error | None:
    if response.status_code == 201:
        response_201 = CreateVirtualMachineOrderResponse201.from_dict(response.json())

        return response_201

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
) -> Response[CreateVirtualMachineOrderResponse201 | Error]:
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
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CreateVirtualMachineOrderResponse201 | Error]:
    """Submit a VM order

     Creates a VM order and invoice through Blesta's canonical order engine. Provisioning still depends
    on the created order being accepted and its invoice being paid. The response echoes the effective
    `Idempotency-Key`. Reusing the same key with the same canonical request body within 24 hours replays
    the original `201` response; reusing it with a different body returns `409 idempotency_key_in_use`.
    A VM order whose resolved OS template is empty (no `template` config option and no package default)
    is rejected at submission with 400 `template_required` before any pending service or invoice is
    created -- supply the `template` config option to resolve this.

    Args:
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (VmOrderRequest): Order request for a new VM. Example: {'package_id': 23,
            'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateVirtualMachineOrderResponse201 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
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
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> CreateVirtualMachineOrderResponse201 | Error | None:
    """Submit a VM order

     Creates a VM order and invoice through Blesta's canonical order engine. Provisioning still depends
    on the created order being accepted and its invoice being paid. The response echoes the effective
    `Idempotency-Key`. Reusing the same key with the same canonical request body within 24 hours replays
    the original `201` response; reusing it with a different body returns `409 idempotency_key_in_use`.
    A VM order whose resolved OS template is empty (no `template` config option and no package default)
    is rejected at submission with 400 `template_required` before any pending service or invoice is
    created -- supply the `template` config option to resolve this.

    Args:
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (VmOrderRequest): Order request for a new VM. Example: {'package_id': 23,
            'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateVirtualMachineOrderResponse201 | Error
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: VmOrderRequest,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CreateVirtualMachineOrderResponse201 | Error]:
    """Submit a VM order

     Creates a VM order and invoice through Blesta's canonical order engine. Provisioning still depends
    on the created order being accepted and its invoice being paid. The response echoes the effective
    `Idempotency-Key`. Reusing the same key with the same canonical request body within 24 hours replays
    the original `201` response; reusing it with a different body returns `409 idempotency_key_in_use`.
    A VM order whose resolved OS template is empty (no `template` config option and no package default)
    is rejected at submission with 400 `template_required` before any pending service or invoice is
    created -- supply the `template` config option to resolve this.

    Args:
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (VmOrderRequest): Order request for a new VM. Example: {'package_id': 23,
            'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateVirtualMachineOrderResponse201 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: VmOrderRequest,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> CreateVirtualMachineOrderResponse201 | Error | None:
    """Submit a VM order

     Creates a VM order and invoice through Blesta's canonical order engine. Provisioning still depends
    on the created order being accepted and its invoice being paid. The response echoes the effective
    `Idempotency-Key`. Reusing the same key with the same canonical request body within 24 hours replays
    the original `201` response; reusing it with a different body returns `409 idempotency_key_in_use`.
    A VM order whose resolved OS template is empty (no `template` config option and no package default)
    is rejected at submission with 400 `template_required` before any pending service or invoice is
    created -- supply the `template` config option to resolve this.

    Args:
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (VmOrderRequest): Order request for a new VM. Example: {'package_id': 23,
            'pricing_id': 12, 'hostname': 'demo1.example.net', 'module_group_id': 4, 'ssh_key': 'ssh-
            ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKDemoKey user@example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateVirtualMachineOrderResponse201 | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
