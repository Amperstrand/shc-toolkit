from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.update_virtual_machine_firewall_rule_response_200 import (
    UpdateVirtualMachineFirewallRuleResponse200,
)
from ...models.vm_firewall_rule_update_request import VmFirewallRuleUpdateRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    pos: int,
    *,
    body: VmFirewallRuleUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/vm/{service_id}/firewall/rules/{pos}".format(
            service_id=quote(str(service_id), safe=""),
            pos=quote(str(pos), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UpdateVirtualMachineFirewallRuleResponse200 | None:
    if response.status_code == 200:
        response_200 = UpdateVirtualMachineFirewallRuleResponse200.from_dict(
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
) -> Response[Error | UpdateVirtualMachineFirewallRuleResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: int,
    pos: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmFirewallRuleUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateVirtualMachineFirewallRuleResponse200]:
    """Edit a firewall rule

     Edits a firewall rule by position within the client-visible set. A position that is absent or
    belongs to a security-group rule returns 404 (existence-hiding).

    Args:
        service_id (int):
        pos (int):
        x_user_api_otp (str | Unset):
        body (VmFirewallRuleUpdateRequest): Edit a firewall rule by position. PATCH semantics:
            only the supplied fields change; at least one recognized field is required.
            `action`/`direction` are NOT required on an edit. The raw Proxmox `type` key is rejected.
            Example: {'enabled': False, 'dest_port': '2222'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateVirtualMachineFirewallRuleResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        pos=pos,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: int,
    pos: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmFirewallRuleUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateVirtualMachineFirewallRuleResponse200 | None:
    """Edit a firewall rule

     Edits a firewall rule by position within the client-visible set. A position that is absent or
    belongs to a security-group rule returns 404 (existence-hiding).

    Args:
        service_id (int):
        pos (int):
        x_user_api_otp (str | Unset):
        body (VmFirewallRuleUpdateRequest): Edit a firewall rule by position. PATCH semantics:
            only the supplied fields change; at least one recognized field is required.
            `action`/`direction` are NOT required on an edit. The raw Proxmox `type` key is rejected.
            Example: {'enabled': False, 'dest_port': '2222'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateVirtualMachineFirewallRuleResponse200
    """

    return sync_detailed(
        service_id=service_id,
        pos=pos,
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    pos: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmFirewallRuleUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateVirtualMachineFirewallRuleResponse200]:
    """Edit a firewall rule

     Edits a firewall rule by position within the client-visible set. A position that is absent or
    belongs to a security-group rule returns 404 (existence-hiding).

    Args:
        service_id (int):
        pos (int):
        x_user_api_otp (str | Unset):
        body (VmFirewallRuleUpdateRequest): Edit a firewall rule by position. PATCH semantics:
            only the supplied fields change; at least one recognized field is required.
            `action`/`direction` are NOT required on an edit. The raw Proxmox `type` key is rejected.
            Example: {'enabled': False, 'dest_port': '2222'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateVirtualMachineFirewallRuleResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        pos=pos,
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    pos: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmFirewallRuleUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateVirtualMachineFirewallRuleResponse200 | None:
    """Edit a firewall rule

     Edits a firewall rule by position within the client-visible set. A position that is absent or
    belongs to a security-group rule returns 404 (existence-hiding).

    Args:
        service_id (int):
        pos (int):
        x_user_api_otp (str | Unset):
        body (VmFirewallRuleUpdateRequest): Edit a firewall rule by position. PATCH semantics:
            only the supplied fields change; at least one recognized field is required.
            `action`/`direction` are NOT required on an edit. The raw Proxmox `type` key is rejected.
            Example: {'enabled': False, 'dest_port': '2222'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateVirtualMachineFirewallRuleResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            pos=pos,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
