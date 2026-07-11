from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_virtual_machine_bandwidth_response_200 import (
    GetVirtualMachineBandwidthResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/vm/{service_id}/bandwidth".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetVirtualMachineBandwidthResponse200 | None:
    if response.status_code == 200:
        response_200 = GetVirtualMachineBandwidthResponse200.from_dict(response.json())

        return response_200

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | GetVirtualMachineBandwidthResponse200]:
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
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetVirtualMachineBandwidthResponse200]:
    """Get VM bandwidth usage

     Returns the stored transfer usage versus the package cap for one owned VM. used_bytes is the
    customer-visible synced figure (service_fields.bandwidth_usage) shown on the portal Manage tab, NOT
    a live RRD recomputation. as_of is the last bandwidth sync timestamp. Unit note: limit_gb uses the
    GB (/1000) convention consistent with GET /vm/{serviceId} specs.bandwidth_gb; the portal Manage
    card's TB label is a display-only quirk.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetVirtualMachineBandwidthResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
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
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetVirtualMachineBandwidthResponse200 | None:
    """Get VM bandwidth usage

     Returns the stored transfer usage versus the package cap for one owned VM. used_bytes is the
    customer-visible synced figure (service_fields.bandwidth_usage) shown on the portal Manage tab, NOT
    a live RRD recomputation. as_of is the last bandwidth sync timestamp. Unit note: limit_gb uses the
    GB (/1000) convention consistent with GET /vm/{serviceId} specs.bandwidth_gb; the portal Manage
    card's TB label is a display-only quirk.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetVirtualMachineBandwidthResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetVirtualMachineBandwidthResponse200]:
    """Get VM bandwidth usage

     Returns the stored transfer usage versus the package cap for one owned VM. used_bytes is the
    customer-visible synced figure (service_fields.bandwidth_usage) shown on the portal Manage tab, NOT
    a live RRD recomputation. as_of is the last bandwidth sync timestamp. Unit note: limit_gb uses the
    GB (/1000) convention consistent with GET /vm/{serviceId} specs.bandwidth_gb; the portal Manage
    card's TB label is a display-only quirk.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetVirtualMachineBandwidthResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetVirtualMachineBandwidthResponse200 | None:
    """Get VM bandwidth usage

     Returns the stored transfer usage versus the package cap for one owned VM. used_bytes is the
    customer-visible synced figure (service_fields.bandwidth_usage) shown on the portal Manage tab, NOT
    a live RRD recomputation. as_of is the last bandwidth sync timestamp. Unit note: limit_gb uses the
    GB (/1000) convention consistent with GET /vm/{serviceId} specs.bandwidth_gb; the portal Manage
    card's TB label is a display-only quirk.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetVirtualMachineBandwidthResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
