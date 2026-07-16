from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.resume_virtual_machine_response_200 import (
    ResumeVirtualMachineResponse200,
)
from ...models.vm_resume_request import VmResumeRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: VmResumeRequest | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    if not isinstance(x_user_api_confirm, Unset):
        headers["X-User-Api-Confirm"] = x_user_api_confirm

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/resume".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ResumeVirtualMachineResponse200 | None:
    if response.status_code == 200:
        response_200 = ResumeVirtualMachineResponse200.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

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
) -> Response[Error | ResumeVirtualMachineResponse200]:
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
    body: VmResumeRequest | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> Response[Error | ResumeVirtualMachineResponse200]:
    """Resume a VM from standby

     Confirm-gated lifecycle operation for an owned parked VM. The first call without X-User-Api-Confirm
    returns 409 confirmation_required. After explicit approval, re-send the byte-identical request with
    the same Idempotency-Key and X-User-Api-Confirm. The API returns the active state plus
    resume_charge. Reusing the same Idempotency-Key with the same body replays the cached response;
    reusing it with a different body returns 422 idempotency_key_conflict.

    Args:
        service_id (int):
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        body (VmResumeRequest | Unset): Optional empty JSON object. A bodyless request is also
            accepted by the live handler.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResumeVirtualMachineResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmResumeRequest | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> Error | ResumeVirtualMachineResponse200 | None:
    """Resume a VM from standby

     Confirm-gated lifecycle operation for an owned parked VM. The first call without X-User-Api-Confirm
    returns 409 confirmation_required. After explicit approval, re-send the byte-identical request with
    the same Idempotency-Key and X-User-Api-Confirm. The API returns the active state plus
    resume_charge. Reusing the same Idempotency-Key with the same body replays the cached response;
    reusing it with a different body returns 422 idempotency_key_conflict.

    Args:
        service_id (int):
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        body (VmResumeRequest | Unset): Optional empty JSON object. A bodyless request is also
            accepted by the live handler.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResumeVirtualMachineResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmResumeRequest | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> Response[Error | ResumeVirtualMachineResponse200]:
    """Resume a VM from standby

     Confirm-gated lifecycle operation for an owned parked VM. The first call without X-User-Api-Confirm
    returns 409 confirmation_required. After explicit approval, re-send the byte-identical request with
    the same Idempotency-Key and X-User-Api-Confirm. The API returns the active state plus
    resume_charge. Reusing the same Idempotency-Key with the same body replays the cached response;
    reusing it with a different body returns 422 idempotency_key_conflict.

    Args:
        service_id (int):
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        body (VmResumeRequest | Unset): Optional empty JSON object. A bodyless request is also
            accepted by the live handler.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResumeVirtualMachineResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: VmResumeRequest | Unset = UNSET,
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
) -> Error | ResumeVirtualMachineResponse200 | None:
    """Resume a VM from standby

     Confirm-gated lifecycle operation for an owned parked VM. The first call without X-User-Api-Confirm
    returns 409 confirmation_required. After explicit approval, re-send the byte-identical request with
    the same Idempotency-Key and X-User-Api-Confirm. The API returns the active state plus
    resume_charge. Reusing the same Idempotency-Key with the same body replays the cached response;
    reusing it with a different body returns 422 idempotency_key_conflict.

    Args:
        service_id (int):
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        body (VmResumeRequest | Unset): Optional empty JSON object. A bodyless request is also
            accepted by the live handler.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResumeVirtualMachineResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
            x_user_api_confirm=x_user_api_confirm,
        )
    ).parsed
