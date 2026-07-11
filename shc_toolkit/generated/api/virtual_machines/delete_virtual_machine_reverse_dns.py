from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_virtual_machine_reverse_dns_body import (
    DeleteVirtualMachineReverseDnsBody,
)
from ...models.delete_virtual_machine_reverse_dns_response_202 import (
    DeleteVirtualMachineReverseDnsResponse202,
)
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: DeleteVirtualMachineReverseDnsBody,
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
        "method": "delete",
        "url": "/vm/{service_id}/rdns".format(
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
) -> DeleteVirtualMachineReverseDnsResponse202 | Error | None:
    if response.status_code == 202:
        response_202 = DeleteVirtualMachineReverseDnsResponse202.from_dict(
            response.json()
        )

        return response_202

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
) -> Response[DeleteVirtualMachineReverseDnsResponse202 | Error]:
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
    body: DeleteVirtualMachineReverseDnsBody,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteVirtualMachineReverseDnsResponse202 | Error]:
    """Clear the PTR for an owned IP

     Clears the reverse-DNS (PTR) record for one owned IP. Applied asynchronously (202 with a job id).

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (DeleteVirtualMachineReverseDnsBody):  Example: {'ip': '203.0.113.45'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteVirtualMachineReverseDnsResponse202 | Error]
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
    body: DeleteVirtualMachineReverseDnsBody,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteVirtualMachineReverseDnsResponse202 | Error | None:
    """Clear the PTR for an owned IP

     Clears the reverse-DNS (PTR) record for one owned IP. Applied asynchronously (202 with a job id).

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (DeleteVirtualMachineReverseDnsBody):  Example: {'ip': '203.0.113.45'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteVirtualMachineReverseDnsResponse202 | Error
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
    body: DeleteVirtualMachineReverseDnsBody,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteVirtualMachineReverseDnsResponse202 | Error]:
    """Clear the PTR for an owned IP

     Clears the reverse-DNS (PTR) record for one owned IP. Applied asynchronously (202 with a job id).

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (DeleteVirtualMachineReverseDnsBody):  Example: {'ip': '203.0.113.45'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteVirtualMachineReverseDnsResponse202 | Error]
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
    body: DeleteVirtualMachineReverseDnsBody,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteVirtualMachineReverseDnsResponse202 | Error | None:
    """Clear the PTR for an owned IP

     Clears the reverse-DNS (PTR) record for one owned IP. Applied asynchronously (202 with a job id).

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (DeleteVirtualMachineReverseDnsBody):  Example: {'ip': '203.0.113.45'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteVirtualMachineReverseDnsResponse202 | Error
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
