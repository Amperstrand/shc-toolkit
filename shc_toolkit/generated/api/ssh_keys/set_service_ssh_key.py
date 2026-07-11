from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.set_service_ssh_key_response_201 import SetServiceSshKeyResponse201
from ...models.set_ssh_key_request import SetSshKeyRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: SetSshKeyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/ssh-key",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | SetServiceSshKeyResponse201 | None:
    if response.status_code == 201:
        response_201 = SetServiceSshKeyResponse201.from_dict(response.json())

        return response_201

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
) -> Response[Error | SetServiceSshKeyResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SetSshKeyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SetServiceSshKeyResponse201]:
    """Set stored SSH key for a service

    Args:
        x_user_api_otp (str | Unset):
        body (SetSshKeyRequest):  Example: {'service_id': 353, 'ssh_key': 'ssh-ed25519
            AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SetServiceSshKeyResponse201]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: SetSshKeyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SetServiceSshKeyResponse201 | None:
    """Set stored SSH key for a service

    Args:
        x_user_api_otp (str | Unset):
        body (SetSshKeyRequest):  Example: {'service_id': 353, 'ssh_key': 'ssh-ed25519
            AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SetServiceSshKeyResponse201
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SetSshKeyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SetServiceSshKeyResponse201]:
    """Set stored SSH key for a service

    Args:
        x_user_api_otp (str | Unset):
        body (SetSshKeyRequest):  Example: {'service_id': 353, 'ssh_key': 'ssh-ed25519
            AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SetServiceSshKeyResponse201]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: SetSshKeyRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SetServiceSshKeyResponse201 | None:
    """Set stored SSH key for a service

    Args:
        x_user_api_otp (str | Unset):
        body (SetSshKeyRequest):  Example: {'service_id': 353, 'ssh_key': 'ssh-ed25519
            AAAAC3NzaC1lZDI1NTE5AAAA... user@host'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SetServiceSshKeyResponse201
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
