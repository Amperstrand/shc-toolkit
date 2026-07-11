from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_service_ssh_key_response_200 import DeleteServiceSshKeyResponse200
from ...models.delete_ssh_key_request import DeleteSshKeyRequest
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DeleteSshKeyRequest,
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
        "url": "/ssh-key",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteServiceSshKeyResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = DeleteServiceSshKeyResponse200.from_dict(response.json())

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
) -> Response[DeleteServiceSshKeyResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DeleteSshKeyRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteServiceSshKeyResponse200 | Error]:
    """Delete stored SSH key for a service

     Deletes one stored SSH public-key entry from the owned service's `ssh_keys` field by fingerprint.
    The operation is idempotent: deleting a fingerprint that is not present still returns 200 with
    `deleted: false`.

    Args:
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (DeleteSshKeyRequest):  Example: {'service_id': 353, 'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteServiceSshKeyResponse200 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: DeleteSshKeyRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteServiceSshKeyResponse200 | Error | None:
    """Delete stored SSH key for a service

     Deletes one stored SSH public-key entry from the owned service's `ssh_keys` field by fingerprint.
    The operation is idempotent: deleting a fingerprint that is not present still returns 200 with
    `deleted: false`.

    Args:
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (DeleteSshKeyRequest):  Example: {'service_id': 353, 'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteServiceSshKeyResponse200 | Error
    """

    return sync_detailed(
        client=client,
        body=body,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DeleteSshKeyRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteServiceSshKeyResponse200 | Error]:
    """Delete stored SSH key for a service

     Deletes one stored SSH public-key entry from the owned service's `ssh_keys` field by fingerprint.
    The operation is idempotent: deleting a fingerprint that is not present still returns 200 with
    `deleted: false`.

    Args:
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (DeleteSshKeyRequest):  Example: {'service_id': 353, 'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteServiceSshKeyResponse200 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: DeleteSshKeyRequest,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteServiceSshKeyResponse200 | Error | None:
    """Delete stored SSH key for a service

     Deletes one stored SSH public-key entry from the owned service's `ssh_keys` field by fingerprint.
    The operation is idempotent: deleting a fingerprint that is not present still returns 200 with
    `deleted: false`.

    Args:
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):
        body (DeleteSshKeyRequest):  Example: {'service_id': 353, 'key_fingerprint':
            'SHA256:W5t8nY2dI0c4XnS7k3P2wM1lQ8r6V9zA0b1C2d3E4fU'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteServiceSshKeyResponse200 | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            confirm=confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
