from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.managed_account_switch_request import ManagedAccountSwitchRequest
from ...models.switch_managed_account_response_200 import (
    SwitchManagedAccountResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    managed_client_id: int,
    *,
    body: ManagedAccountSwitchRequest,
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
        "url": "/managed-accounts/{managed_client_id}/switch".format(
            managed_client_id=quote(str(managed_client_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | SwitchManagedAccountResponse200 | None:
    if response.status_code == 200:
        response_200 = SwitchManagedAccountResponse200.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | SwitchManagedAccountResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    managed_client_id: int,
    *,
    client: AuthenticatedClient,
    body: ManagedAccountSwitchRequest,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SwitchManagedAccountResponse200]:
    """Switch into a managed account

     Validates a dual-identity managed-account act-as context for a Blesta-native manager relationship.
    The authenticated manager must have an accepted invitation and contact_permissions grant on the
    managed client, both clients must belong to the same company, and each requested area must already
    be granted. Send the returned X-Managed-Client-Id on later calls; those calls are evaluated under
    the managed client's identity but never outside the approved area set.

    Args:
        managed_client_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (ManagedAccountSwitchRequest): Managed-account switch request. The requested areas
            are intersected with the Blesta-native manager grants; ungranted areas are rejected.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SwitchManagedAccountResponse200]
    """

    kwargs = _get_kwargs(
        managed_client_id=managed_client_id,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    managed_client_id: int,
    *,
    client: AuthenticatedClient,
    body: ManagedAccountSwitchRequest,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SwitchManagedAccountResponse200 | None:
    """Switch into a managed account

     Validates a dual-identity managed-account act-as context for a Blesta-native manager relationship.
    The authenticated manager must have an accepted invitation and contact_permissions grant on the
    managed client, both clients must belong to the same company, and each requested area must already
    be granted. Send the returned X-Managed-Client-Id on later calls; those calls are evaluated under
    the managed client's identity but never outside the approved area set.

    Args:
        managed_client_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (ManagedAccountSwitchRequest): Managed-account switch request. The requested areas
            are intersected with the Blesta-native manager grants; ungranted areas are rejected.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SwitchManagedAccountResponse200
    """

    return sync_detailed(
        managed_client_id=managed_client_id,
        client=client,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    managed_client_id: int,
    *,
    client: AuthenticatedClient,
    body: ManagedAccountSwitchRequest,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | SwitchManagedAccountResponse200]:
    """Switch into a managed account

     Validates a dual-identity managed-account act-as context for a Blesta-native manager relationship.
    The authenticated manager must have an accepted invitation and contact_permissions grant on the
    managed client, both clients must belong to the same company, and each requested area must already
    be granted. Send the returned X-Managed-Client-Id on later calls; those calls are evaluated under
    the managed client's identity but never outside the approved area set.

    Args:
        managed_client_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (ManagedAccountSwitchRequest): Managed-account switch request. The requested areas
            are intersected with the Blesta-native manager grants; ungranted areas are rejected.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SwitchManagedAccountResponse200]
    """

    kwargs = _get_kwargs(
        managed_client_id=managed_client_id,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    managed_client_id: int,
    *,
    client: AuthenticatedClient,
    body: ManagedAccountSwitchRequest,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | SwitchManagedAccountResponse200 | None:
    """Switch into a managed account

     Validates a dual-identity managed-account act-as context for a Blesta-native manager relationship.
    The authenticated manager must have an accepted invitation and contact_permissions grant on the
    managed client, both clients must belong to the same company, and each requested area must already
    be granted. Send the returned X-Managed-Client-Id on later calls; those calls are evaluated under
    the managed client's identity but never outside the approved area set.

    Args:
        managed_client_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (ManagedAccountSwitchRequest): Managed-account switch request. The requested areas
            are intersected with the Blesta-native manager grants; ungranted areas are rejected.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SwitchManagedAccountResponse200
    """

    return (
        await asyncio_detailed(
            managed_client_id=managed_client_id,
            client=client,
            body=body,
            x_user_api_confirm=x_user_api_confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
