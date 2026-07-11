from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_activity_list import AccountActivityList
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/account/activity",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AccountActivityList | Error | None:
    if response.status_code == 200:
        response_200 = AccountActivityList.from_dict(response.json())

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
) -> Response[AccountActivityList | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[AccountActivityList | Error]:
    """List account activity

     Read-only, client-scoped account audit log merged most-recent-first from Blesta's native logs: the
    authenticated client's own sign-ins (success + failed), account/contact detail changes, account-
    setting changes, and payment/transaction activity (ActivityItem types login, login_failed,
    contact_change, setting_change, transaction). Returns only non-sensitive fields (event type,
    timestamp, the client's own source IP for logins, and-for contact/setting changes-the NAMES and a
    count of changed fields, never their values). Never returns another tenant's activity, internal
    user/staff ids, or placement.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountActivityList | Error]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> AccountActivityList | Error | None:
    """List account activity

     Read-only, client-scoped account audit log merged most-recent-first from Blesta's native logs: the
    authenticated client's own sign-ins (success + failed), account/contact detail changes, account-
    setting changes, and payment/transaction activity (ActivityItem types login, login_failed,
    contact_change, setting_change, transaction). Returns only non-sensitive fields (event type,
    timestamp, the client's own source IP for logins, and-for contact/setting changes-the NAMES and a
    count of changed fields, never their values). Never returns another tenant's activity, internal
    user/staff ids, or placement.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountActivityList | Error
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[AccountActivityList | Error]:
    """List account activity

     Read-only, client-scoped account audit log merged most-recent-first from Blesta's native logs: the
    authenticated client's own sign-ins (success + failed), account/contact detail changes, account-
    setting changes, and payment/transaction activity (ActivityItem types login, login_failed,
    contact_change, setting_change, transaction). Returns only non-sensitive fields (event type,
    timestamp, the client's own source IP for logins, and-for contact/setting changes-the NAMES and a
    count of changed fields, never their values). Never returns another tenant's activity, internal
    user/staff ids, or placement.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountActivityList | Error]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> AccountActivityList | Error | None:
    """List account activity

     Read-only, client-scoped account audit log merged most-recent-first from Blesta's native logs: the
    authenticated client's own sign-ins (success + failed), account/contact detail changes, account-
    setting changes, and payment/transaction activity (ActivityItem types login, login_failed,
    contact_change, setting_change, transaction). Returns only non-sensitive fields (event type,
    timestamp, the client's own source IP for logins, and-for contact/setting changes-the NAMES and a
    count of changed fields, never their values). Never returns another tenant's activity, internal
    user/staff ids, or placement.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountActivityList | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
