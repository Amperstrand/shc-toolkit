from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cancel_virtual_machine_response_200 import (
    CancelVirtualMachineResponse200,
)
from ...models.cancel_vm_request import CancelVmRequest
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: CancelVmRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["confirm"] = confirm

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/cancel".format(
            service_id=quote(str(service_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CancelVirtualMachineResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = CancelVirtualMachineResponse200.from_dict(response.json())

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
) -> Response[CancelVirtualMachineResponse200 | Error]:
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
    body: CancelVmRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CancelVirtualMachineResponse200 | Error]:
    """Cancel a VM service

     Schedules customer-initiated cancellation for an owned VM service. By default the service is
    canceled at the end of the current term; set `immediate` to `true` to cancel it now and release
    resources immediately.

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (CancelVmRequest):  Example: {'reason': 'Service no longer needed after migration.',
            'immediate': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelVirtualMachineResponse200 | Error]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        confirm=confirm,
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
    body: CancelVmRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> CancelVirtualMachineResponse200 | Error | None:
    """Cancel a VM service

     Schedules customer-initiated cancellation for an owned VM service. By default the service is
    canceled at the end of the current term; set `immediate` to `true` to cancel it now and release
    resources immediately.

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (CancelVmRequest):  Example: {'reason': 'Service no longer needed after migration.',
            'immediate': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelVirtualMachineResponse200 | Error
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CancelVmRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CancelVirtualMachineResponse200 | Error]:
    """Cancel a VM service

     Schedules customer-initiated cancellation for an owned VM service. By default the service is
    canceled at the end of the current term; set `immediate` to `true` to cancel it now and release
    resources immediately.

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (CancelVmRequest):  Example: {'reason': 'Service no longer needed after migration.',
            'immediate': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelVirtualMachineResponse200 | Error]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CancelVmRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> CancelVirtualMachineResponse200 | Error | None:
    """Cancel a VM service

     Schedules customer-initiated cancellation for an owned VM service. By default the service is
    canceled at the end of the current term; set `immediate` to `true` to cancel it now and release
    resources immediately.

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (CancelVmRequest):  Example: {'reason': 'Service no longer needed after migration.',
            'immediate': False}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelVirtualMachineResponse200 | Error
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            confirm=confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
