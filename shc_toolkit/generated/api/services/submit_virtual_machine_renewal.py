from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.submit_virtual_machine_renewal_body import (
    SubmitVirtualMachineRenewalBody,
)
from ...models.submit_virtual_machine_renewal_response_201 import (
    SubmitVirtualMachineRenewalResponse201,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: SubmitVirtualMachineRenewalBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_confirm, Unset):
        headers["X-User-Api-Confirm"] = x_user_api_confirm

    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/renew".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | SubmitVirtualMachineRenewalResponse201 | None:
    if response.status_code == 201:
        response_201 = SubmitVirtualMachineRenewalResponse201.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | SubmitVirtualMachineRenewalResponse201]:
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
    body: SubmitVirtualMachineRenewalBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SubmitVirtualMachineRenewalResponse201]:
    """Commit a service renewal

     Renews an owned service (optionally into a different term if the account permits) and returns the
    renewal invoice as a checkout pointer. Confirm-gated spend; idempotent by idempotency_key. The
    service renews when the invoice is paid.

    Args:
        service_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (SubmitVirtualMachineRenewalBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SubmitVirtualMachineRenewalResponse201]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
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
    body: SubmitVirtualMachineRenewalBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SubmitVirtualMachineRenewalResponse201 | None:
    """Commit a service renewal

     Renews an owned service (optionally into a different term if the account permits) and returns the
    renewal invoice as a checkout pointer. Confirm-gated spend; idempotent by idempotency_key. The
    service renews when the invoice is paid.

    Args:
        service_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (SubmitVirtualMachineRenewalBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SubmitVirtualMachineRenewalResponse201
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: SubmitVirtualMachineRenewalBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SubmitVirtualMachineRenewalResponse201]:
    """Commit a service renewal

     Renews an owned service (optionally into a different term if the account permits) and returns the
    renewal invoice as a checkout pointer. Confirm-gated spend; idempotent by idempotency_key. The
    service renews when the invoice is paid.

    Args:
        service_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (SubmitVirtualMachineRenewalBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SubmitVirtualMachineRenewalResponse201]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: SubmitVirtualMachineRenewalBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SubmitVirtualMachineRenewalResponse201 | None:
    """Commit a service renewal

     Renews an owned service (optionally into a different term if the account permits) and returns the
    renewal invoice as a checkout pointer. Confirm-gated spend; idempotent by idempotency_key. The
    service renews when the invoice is paid.

    Args:
        service_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (SubmitVirtualMachineRenewalBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SubmitVirtualMachineRenewalResponse201
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            x_user_api_confirm=x_user_api_confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
