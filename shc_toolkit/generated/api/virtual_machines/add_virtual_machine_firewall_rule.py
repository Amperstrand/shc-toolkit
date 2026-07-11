from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_virtual_machine_firewall_rule_response_201 import (
    AddVirtualMachineFirewallRuleResponse201,
)
from ...models.error import Error
from ...models.vm_firewall_rule_create_request import VmFirewallRuleCreateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: VmFirewallRuleCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/firewall/rules".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AddVirtualMachineFirewallRuleResponse201 | Error | None:
    if response.status_code == 201:
        response_201 = AddVirtualMachineFirewallRuleResponse201.from_dict(
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
) -> Response[AddVirtualMachineFirewallRuleResponse201 | Error]:
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
    body: VmFirewallRuleCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[AddVirtualMachineFirewallRuleResponse201 | Error]:
    """Create a firewall rule

     Appends a firewall rule to the VM. Security-group rules cannot be created via the API. Returns the
    refreshed client-visible rule list.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmFirewallRuleCreateRequest): Create a firewall rule. `action` and `direction` are
            required; all other fields are optional. The raw Proxmox `type` key is rejected (use
            `direction`). Example: {'action': 'DROP', 'direction': 'in', 'source': '203.0.113.99',
            'name': 'block-scanner'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddVirtualMachineFirewallRuleResponse201 | Error]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
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
    body: VmFirewallRuleCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> AddVirtualMachineFirewallRuleResponse201 | Error | None:
    """Create a firewall rule

     Appends a firewall rule to the VM. Security-group rules cannot be created via the API. Returns the
    refreshed client-visible rule list.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmFirewallRuleCreateRequest): Create a firewall rule. `action` and `direction` are
            required; all other fields are optional. The raw Proxmox `type` key is rejected (use
            `direction`). Example: {'action': 'DROP', 'direction': 'in', 'source': '203.0.113.99',
            'name': 'block-scanner'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddVirtualMachineFirewallRuleResponse201 | Error
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmFirewallRuleCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[AddVirtualMachineFirewallRuleResponse201 | Error]:
    """Create a firewall rule

     Appends a firewall rule to the VM. Security-group rules cannot be created via the API. Returns the
    refreshed client-visible rule list.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmFirewallRuleCreateRequest): Create a firewall rule. `action` and `direction` are
            required; all other fields are optional. The raw Proxmox `type` key is rejected (use
            `direction`). Example: {'action': 'DROP', 'direction': 'in', 'source': '203.0.113.99',
            'name': 'block-scanner'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddVirtualMachineFirewallRuleResponse201 | Error]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmFirewallRuleCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> AddVirtualMachineFirewallRuleResponse201 | Error | None:
    """Create a firewall rule

     Appends a firewall rule to the VM. Security-group rules cannot be created via the API. Returns the
    refreshed client-visible rule list.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmFirewallRuleCreateRequest): Create a firewall rule. `action` and `direction` are
            required; all other fields are optional. The raw Proxmox `type` key is rejected (use
            `direction`). Example: {'action': 'DROP', 'direction': 'in', 'source': '203.0.113.99',
            'name': 'block-scanner'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddVirtualMachineFirewallRuleResponse201 | Error
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
