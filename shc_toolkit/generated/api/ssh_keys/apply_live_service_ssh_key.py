from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apply_live_service_ssh_key_response_200 import (
    ApplyLiveServiceSshKeyResponse200,
)
from ...models.error import Error
from ...models.vm_ssh_key_apply_live_request import VmSshKeyApplyLiveRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: VmSshKeyApplyLiveRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/ssh-keys/apply-live".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApplyLiveServiceSshKeyResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = ApplyLiveServiceSshKeyResponse200.from_dict(response.json())

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
) -> Response[ApplyLiveServiceSshKeyResponse200 | Error]:
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
    body: VmSshKeyApplyLiveRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[ApplyLiveServiceSshKeyResponse200 | Error]:
    """Live-inject an SSH key into a running VM

     Injects a single-line SSH public key into the running VM via the guest agent (best-effort) and
    persists it so a later reinstall keeps it. The VM must be running. The live inject is not
    authoritatively confirmable, so the response reports `live_inject: attempted`.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmSshKeyApplyLiveRequest): Live-inject a single-line SSH public key into the running
            VM via the guest agent. The key is also persisted so a later reinstall keeps it. Example:
            {'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApplyLiveServiceSshKeyResponse200 | Error]
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
    body: VmSshKeyApplyLiveRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> ApplyLiveServiceSshKeyResponse200 | Error | None:
    """Live-inject an SSH key into a running VM

     Injects a single-line SSH public key into the running VM via the guest agent (best-effort) and
    persists it so a later reinstall keeps it. The VM must be running. The live inject is not
    authoritatively confirmable, so the response reports `live_inject: attempted`.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmSshKeyApplyLiveRequest): Live-inject a single-line SSH public key into the running
            VM via the guest agent. The key is also persisted so a later reinstall keeps it. Example:
            {'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApplyLiveServiceSshKeyResponse200 | Error
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
    body: VmSshKeyApplyLiveRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[ApplyLiveServiceSshKeyResponse200 | Error]:
    """Live-inject an SSH key into a running VM

     Injects a single-line SSH public key into the running VM via the guest agent (best-effort) and
    persists it so a later reinstall keeps it. The VM must be running. The live inject is not
    authoritatively confirmable, so the response reports `live_inject: attempted`.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmSshKeyApplyLiveRequest): Live-inject a single-line SSH public key into the running
            VM via the guest agent. The key is also persisted so a later reinstall keeps it. Example:
            {'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApplyLiveServiceSshKeyResponse200 | Error]
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
    body: VmSshKeyApplyLiveRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> ApplyLiveServiceSshKeyResponse200 | Error | None:
    """Live-inject an SSH key into a running VM

     Injects a single-line SSH public key into the running VM via the guest agent (best-effort) and
    persists it so a later reinstall keeps it. The VM must be running. The live inject is not
    authoritatively confirmable, so the response reports `live_inject: attempted`.

    Args:
        service_id (int):
        x_user_api_otp (str | Unset):
        body (VmSshKeyApplyLiveRequest): Live-inject a single-line SSH public key into the running
            VM via the guest agent. The key is also persisted so a later reinstall keeps it. Example:
            {'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApplyLiveServiceSshKeyResponse200 | Error
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
