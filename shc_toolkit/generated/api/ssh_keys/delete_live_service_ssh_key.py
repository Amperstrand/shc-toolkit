from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_live_service_ssh_key_response_200 import (
    DeleteLiveServiceSshKeyResponse200,
)
from ...models.error import Error
from ...models.vm_ssh_key_delete_live_request import VmSshKeyDeleteLiveRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: VmSshKeyDeleteLiveRequest,
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
        "url": "/vm/{service_id}/ssh-keys/live".format(
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
) -> DeleteLiveServiceSshKeyResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = DeleteLiveServiceSshKeyResponse200.from_dict(response.json())

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
) -> Response[DeleteLiveServiceSshKeyResponse200 | Error]:
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
    body: VmSshKeyDeleteLiveRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteLiveServiceSshKeyResponse200 | Error]:
    """Live-remove an SSH key from a running VM

     Removes an SSH key from the running VM by fingerprint (best-effort guest-exec) and scrubs it from
    the persisted set. The VM must be running. Idempotent: removing a fingerprint that is not present
    returns 200 with `removed: false`. The request carries a JSON body.

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (VmSshKeyDeleteLiveRequest): Live-remove an SSH key from the running VM by
            fingerprint, and scrub it from the persisted set. Example: {'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteLiveServiceSshKeyResponse200 | Error]
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
    body: VmSshKeyDeleteLiveRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteLiveServiceSshKeyResponse200 | Error | None:
    """Live-remove an SSH key from a running VM

     Removes an SSH key from the running VM by fingerprint (best-effort guest-exec) and scrubs it from
    the persisted set. The VM must be running. Idempotent: removing a fingerprint that is not present
    returns 200 with `removed: false`. The request carries a JSON body.

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (VmSshKeyDeleteLiveRequest): Live-remove an SSH key from the running VM by
            fingerprint, and scrub it from the persisted set. Example: {'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteLiveServiceSshKeyResponse200 | Error
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
    body: VmSshKeyDeleteLiveRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteLiveServiceSshKeyResponse200 | Error]:
    """Live-remove an SSH key from a running VM

     Removes an SSH key from the running VM by fingerprint (best-effort guest-exec) and scrubs it from
    the persisted set. The VM must be running. Idempotent: removing a fingerprint that is not present
    returns 200 with `removed: false`. The request carries a JSON body.

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (VmSshKeyDeleteLiveRequest): Live-remove an SSH key from the running VM by
            fingerprint, and scrub it from the persisted set. Example: {'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteLiveServiceSshKeyResponse200 | Error]
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
    body: VmSshKeyDeleteLiveRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteLiveServiceSshKeyResponse200 | Error | None:
    """Live-remove an SSH key from a running VM

     Removes an SSH key from the running VM by fingerprint (best-effort guest-exec) and scrubs it from
    the persisted set. The VM must be running. Idempotent: removing a fingerprint that is not present
    returns 200 with `removed: false`. The request carries a JSON body.

    Args:
        service_id (int):
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (VmSshKeyDeleteLiveRequest): Live-remove an SSH key from the running VM by
            fingerprint, and scrub it from the persisted set. Example: {'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteLiveServiceSshKeyResponse200 | Error
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
