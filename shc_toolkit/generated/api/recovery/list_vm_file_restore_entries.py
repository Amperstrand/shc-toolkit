from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_vm_file_restore_entries_response_200 import (
    ListVmFileRestoreEntriesResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    backup_id: str,
    storage: str | Unset = UNSET,
    filepath: str | Unset = "/",
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["backup_id"] = backup_id

    params["storage"] = storage

    params["filepath"] = filepath

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/vm/{service_id}/file-restore/list".format(
            service_id=quote(str(service_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListVmFileRestoreEntriesResponse200 | None:
    if response.status_code == 200:
        response_200 = ListVmFileRestoreEntriesResponse200.from_dict(response.json())

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
) -> Response[Error | ListVmFileRestoreEntriesResponse200]:
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
    backup_id: str,
    storage: str | Unset = UNSET,
    filepath: str | Unset = "/",
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListVmFileRestoreEntriesResponse200]:
    """Browse files in a restore point

     Lists directory entries within a chosen restore point via PBS file-restore for one owned VM service.
    The `backup_id` is hard-scoped to this VM. When `filepath` is omitted or `/`, the listing auto-
    navigates through the PBS disk/partition layers to the filesystem root. Single-object response (one
    directory listing), not a paginated collection.

    Args:
        service_id (int):
        backup_id (str):  Example: bk_6ERwSd_PLY66FW72VFM.
        storage (str | Unset):
        filepath (str | Unset):  Default: '/'.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListVmFileRestoreEntriesResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        backup_id=backup_id,
        storage=storage,
        filepath=filepath,
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
    backup_id: str,
    storage: str | Unset = UNSET,
    filepath: str | Unset = "/",
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListVmFileRestoreEntriesResponse200 | None:
    """Browse files in a restore point

     Lists directory entries within a chosen restore point via PBS file-restore for one owned VM service.
    The `backup_id` is hard-scoped to this VM. When `filepath` is omitted or `/`, the listing auto-
    navigates through the PBS disk/partition layers to the filesystem root. Single-object response (one
    directory listing), not a paginated collection.

    Args:
        service_id (int):
        backup_id (str):  Example: bk_6ERwSd_PLY66FW72VFM.
        storage (str | Unset):
        filepath (str | Unset):  Default: '/'.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListVmFileRestoreEntriesResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        backup_id=backup_id,
        storage=storage,
        filepath=filepath,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    backup_id: str,
    storage: str | Unset = UNSET,
    filepath: str | Unset = "/",
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListVmFileRestoreEntriesResponse200]:
    """Browse files in a restore point

     Lists directory entries within a chosen restore point via PBS file-restore for one owned VM service.
    The `backup_id` is hard-scoped to this VM. When `filepath` is omitted or `/`, the listing auto-
    navigates through the PBS disk/partition layers to the filesystem root. Single-object response (one
    directory listing), not a paginated collection.

    Args:
        service_id (int):
        backup_id (str):  Example: bk_6ERwSd_PLY66FW72VFM.
        storage (str | Unset):
        filepath (str | Unset):  Default: '/'.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListVmFileRestoreEntriesResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        backup_id=backup_id,
        storage=storage,
        filepath=filepath,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    backup_id: str,
    storage: str | Unset = UNSET,
    filepath: str | Unset = "/",
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListVmFileRestoreEntriesResponse200 | None:
    """Browse files in a restore point

     Lists directory entries within a chosen restore point via PBS file-restore for one owned VM service.
    The `backup_id` is hard-scoped to this VM. When `filepath` is omitted or `/`, the listing auto-
    navigates through the PBS disk/partition layers to the filesystem root. Single-object response (one
    directory listing), not a paginated collection.

    Args:
        service_id (int):
        backup_id (str):  Example: bk_6ERwSd_PLY66FW72VFM.
        storage (str | Unset):
        filepath (str | Unset):  Default: '/'.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListVmFileRestoreEntriesResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            backup_id=backup_id,
            storage=storage,
            filepath=filepath,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
