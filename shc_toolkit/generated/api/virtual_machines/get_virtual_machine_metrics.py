from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_virtual_machine_metrics_response_200 import (
    GetVirtualMachineMetricsResponse200,
)
from ...models.get_virtual_machine_metrics_timeframe import (
    GetVirtualMachineMetricsTimeframe,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    timeframe: GetVirtualMachineMetricsTimeframe
    | Unset = GetVirtualMachineMetricsTimeframe.HOUR,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    json_timeframe: str | Unset = UNSET
    if not isinstance(timeframe, Unset):
        json_timeframe = timeframe.value

    params["timeframe"] = json_timeframe

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/vm/{service_id}/metrics".format(
            service_id=quote(str(service_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetVirtualMachineMetricsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetVirtualMachineMetricsResponse200.from_dict(response.json())

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
) -> Response[Error | GetVirtualMachineMetricsResponse200]:
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
    timeframe: GetVirtualMachineMetricsTimeframe
    | Unset = GetVirtualMachineMetricsTimeframe.HOUR,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetVirtualMachineMetricsResponse200]:
    """Get VM time-series metrics

     Returns Proxmox RRD time-series for CPU, RAM, disk read/write, and network in/out for one owned VM.
    Mirrors the client portal Manage tab charts (consolidation is fixed to MAX server-side). Each series
    is an array of [epoch_seconds, value] pairs; dividers convert raw values to display units (RAM
    bytes->GiB, disk/network bytes->MiB). A freshly provisioned VM may return empty value arrays. Data
    before the current provisioning generation (last_install) is filtered out.

    Args:
        service_id (int):
        timeframe (GetVirtualMachineMetricsTimeframe | Unset):  Default:
            GetVirtualMachineMetricsTimeframe.HOUR.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetVirtualMachineMetricsResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        timeframe=timeframe,
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
    timeframe: GetVirtualMachineMetricsTimeframe
    | Unset = GetVirtualMachineMetricsTimeframe.HOUR,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetVirtualMachineMetricsResponse200 | None:
    """Get VM time-series metrics

     Returns Proxmox RRD time-series for CPU, RAM, disk read/write, and network in/out for one owned VM.
    Mirrors the client portal Manage tab charts (consolidation is fixed to MAX server-side). Each series
    is an array of [epoch_seconds, value] pairs; dividers convert raw values to display units (RAM
    bytes->GiB, disk/network bytes->MiB). A freshly provisioned VM may return empty value arrays. Data
    before the current provisioning generation (last_install) is filtered out.

    Args:
        service_id (int):
        timeframe (GetVirtualMachineMetricsTimeframe | Unset):  Default:
            GetVirtualMachineMetricsTimeframe.HOUR.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetVirtualMachineMetricsResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        timeframe=timeframe,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    timeframe: GetVirtualMachineMetricsTimeframe
    | Unset = GetVirtualMachineMetricsTimeframe.HOUR,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetVirtualMachineMetricsResponse200]:
    """Get VM time-series metrics

     Returns Proxmox RRD time-series for CPU, RAM, disk read/write, and network in/out for one owned VM.
    Mirrors the client portal Manage tab charts (consolidation is fixed to MAX server-side). Each series
    is an array of [epoch_seconds, value] pairs; dividers convert raw values to display units (RAM
    bytes->GiB, disk/network bytes->MiB). A freshly provisioned VM may return empty value arrays. Data
    before the current provisioning generation (last_install) is filtered out.

    Args:
        service_id (int):
        timeframe (GetVirtualMachineMetricsTimeframe | Unset):  Default:
            GetVirtualMachineMetricsTimeframe.HOUR.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetVirtualMachineMetricsResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        timeframe=timeframe,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    timeframe: GetVirtualMachineMetricsTimeframe
    | Unset = GetVirtualMachineMetricsTimeframe.HOUR,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetVirtualMachineMetricsResponse200 | None:
    """Get VM time-series metrics

     Returns Proxmox RRD time-series for CPU, RAM, disk read/write, and network in/out for one owned VM.
    Mirrors the client portal Manage tab charts (consolidation is fixed to MAX server-side). Each series
    is an array of [epoch_seconds, value] pairs; dividers convert raw values to display units (RAM
    bytes->GiB, disk/network bytes->MiB). A freshly provisioned VM may return empty value arrays. Data
    before the current provisioning generation (last_install) is filtered out.

    Args:
        service_id (int):
        timeframe (GetVirtualMachineMetricsTimeframe | Unset):  Default:
            GetVirtualMachineMetricsTimeframe.HOUR.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetVirtualMachineMetricsResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            timeframe=timeframe,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
