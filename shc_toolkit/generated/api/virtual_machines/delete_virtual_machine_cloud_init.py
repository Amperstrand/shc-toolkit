from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_virtual_machine_cloud_init_body import (
    DeleteVirtualMachineCloudInitBody,
)
from ...models.delete_virtual_machine_cloud_init_response_200 import (
    DeleteVirtualMachineCloudInitResponse200,
)
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    virtual_machine_id: int,
    *,
    body: DeleteVirtualMachineCloudInitBody | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    if not isinstance(x_user_api_confirm, Unset):
        headers["X-User-Api-Confirm"] = x_user_api_confirm

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/virtual-machines/{virtual_machine_id}/cloud-init".format(
            virtual_machine_id=quote(str(virtual_machine_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteVirtualMachineCloudInitResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = DeleteVirtualMachineCloudInitResponse200.from_dict(
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
) -> Response[DeleteVirtualMachineCloudInitResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    virtual_machine_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteVirtualMachineCloudInitBody | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> Response[DeleteVirtualMachineCloudInitResponse200 | Error]:
    """Revert VM cloud-init user-data

     Confirm-gated cloud-init revert. Detaches the derived NoCloud CD-ROM ISO, removes the server-managed
    seed, and restores the provider-managed cloud-init attachment.

    Args:
        virtual_machine_id (int):
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        body (DeleteVirtualMachineCloudInitBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteVirtualMachineCloudInitResponse200 | Error]
    """

    kwargs = _get_kwargs(
        virtual_machine_id=virtual_machine_id,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    virtual_machine_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteVirtualMachineCloudInitBody | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> DeleteVirtualMachineCloudInitResponse200 | Error | None:
    """Revert VM cloud-init user-data

     Confirm-gated cloud-init revert. Detaches the derived NoCloud CD-ROM ISO, removes the server-managed
    seed, and restores the provider-managed cloud-init attachment.

    Args:
        virtual_machine_id (int):
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        body (DeleteVirtualMachineCloudInitBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteVirtualMachineCloudInitResponse200 | Error
    """

    return sync_detailed(
        virtual_machine_id=virtual_machine_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
    ).parsed


async def asyncio_detailed(
    virtual_machine_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteVirtualMachineCloudInitBody | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> Response[DeleteVirtualMachineCloudInitResponse200 | Error]:
    """Revert VM cloud-init user-data

     Confirm-gated cloud-init revert. Detaches the derived NoCloud CD-ROM ISO, removes the server-managed
    seed, and restores the provider-managed cloud-init attachment.

    Args:
        virtual_machine_id (int):
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        body (DeleteVirtualMachineCloudInitBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteVirtualMachineCloudInitResponse200 | Error]
    """

    kwargs = _get_kwargs(
        virtual_machine_id=virtual_machine_id,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    virtual_machine_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteVirtualMachineCloudInitBody | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> DeleteVirtualMachineCloudInitResponse200 | Error | None:
    """Revert VM cloud-init user-data

     Confirm-gated cloud-init revert. Detaches the derived NoCloud CD-ROM ISO, removes the server-managed
    seed, and restores the provider-managed cloud-init attachment.

    Args:
        virtual_machine_id (int):
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        body (DeleteVirtualMachineCloudInitBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteVirtualMachineCloudInitResponse200 | Error
    """

    return (
        await asyncio_detailed(
            virtual_machine_id=virtual_machine_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
            x_user_api_confirm=x_user_api_confirm,
        )
    ).parsed
