from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_virtual_machine_activity_response_200 import (
    ListVirtualMachineActivityResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/vm/{service_id}/activity".format(
            service_id=quote(str(service_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListVirtualMachineActivityResponse200 | None:
    if response.status_code == 200:
        response_200 = ListVirtualMachineActivityResponse200.from_dict(response.json())

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
) -> Response[Error | ListVirtualMachineActivityResponse200]:
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
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListVirtualMachineActivityResponse200]:
    """List VM activity (Proxmox task history)

     Lists the live Proxmox node task history for one owned VM (qmstart, qmstop, vzdump, etc.), scoped to
    the current provisioning generation. This is distinct from GET /vm/{serviceId}/jobs, which lists
    Blesta-side background jobs. Each item carries only command type, start/finish times, and status;
    infrastructure identifiers (UPID/node/PID/PVE user) are stripped. pagination.total is best-effort
    (Proxmox does not return a reliable count) — treat the X-User-Api-Has-More header as authoritative
    for whether another page exists. Capped at 100 items per page.

    Args:
        service_id (int):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListVirtualMachineActivityResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        limit=limit,
        offset=offset,
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
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListVirtualMachineActivityResponse200 | None:
    """List VM activity (Proxmox task history)

     Lists the live Proxmox node task history for one owned VM (qmstart, qmstop, vzdump, etc.), scoped to
    the current provisioning generation. This is distinct from GET /vm/{serviceId}/jobs, which lists
    Blesta-side background jobs. Each item carries only command type, start/finish times, and status;
    infrastructure identifiers (UPID/node/PID/PVE user) are stripped. pagination.total is best-effort
    (Proxmox does not return a reliable count) — treat the X-User-Api-Has-More header as authoritative
    for whether another page exists. Capped at 100 items per page.

    Args:
        service_id (int):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListVirtualMachineActivityResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListVirtualMachineActivityResponse200]:
    """List VM activity (Proxmox task history)

     Lists the live Proxmox node task history for one owned VM (qmstart, qmstop, vzdump, etc.), scoped to
    the current provisioning generation. This is distinct from GET /vm/{serviceId}/jobs, which lists
    Blesta-side background jobs. Each item carries only command type, start/finish times, and status;
    infrastructure identifiers (UPID/node/PID/PVE user) are stripped. pagination.total is best-effort
    (Proxmox does not return a reliable count) — treat the X-User-Api-Has-More header as authoritative
    for whether another page exists. Capped at 100 items per page.

    Args:
        service_id (int):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListVirtualMachineActivityResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListVirtualMachineActivityResponse200 | None:
    """List VM activity (Proxmox task history)

     Lists the live Proxmox node task history for one owned VM (qmstart, qmstop, vzdump, etc.), scoped to
    the current provisioning generation. This is distinct from GET /vm/{serviceId}/jobs, which lists
    Blesta-side background jobs. Each item carries only command type, start/finish times, and status;
    infrastructure identifiers (UPID/node/PID/PVE user) are stripped. pagination.total is best-effort
    (Proxmox does not return a reliable count) — treat the X-User-Api-Has-More header as authoritative
    for whether another page exists. Capped at 100 items per page.

    Args:
        service_id (int):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListVirtualMachineActivityResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            limit=limit,
            offset=offset,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
