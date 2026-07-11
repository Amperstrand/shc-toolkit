import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_invoices_response_200 import ListInvoicesResponse200
from ...models.list_invoices_status import ListInvoicesStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    status: ListInvoicesStatus | Unset = ListInvoicesStatus.OPEN,
    currency: str | Unset = UNSET,
    date_due_start: datetime.date | Unset = UNSET,
    date_due_end: datetime.date | Unset = UNSET,
    min_amount: float | Unset = UNSET,
    max_amount: float | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["currency"] = currency

    json_date_due_start: str | Unset = UNSET
    if not isinstance(date_due_start, Unset):
        json_date_due_start = date_due_start.isoformat()
    params["date_due_start"] = json_date_due_start

    json_date_due_end: str | Unset = UNSET
    if not isinstance(date_due_end, Unset):
        json_date_due_end = date_due_end.isoformat()
    params["date_due_end"] = json_date_due_end

    params["min_amount"] = min_amount

    params["max_amount"] = max_amount

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/invoices",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListInvoicesResponse200 | None:
    if response.status_code == 200:
        response_200 = ListInvoicesResponse200.from_dict(response.json())

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
) -> Response[Error | ListInvoicesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    status: ListInvoicesStatus | Unset = ListInvoicesStatus.OPEN,
    currency: str | Unset = UNSET,
    date_due_start: datetime.date | Unset = UNSET,
    date_due_end: datetime.date | Unset = UNSET,
    min_amount: float | Unset = UNSET,
    max_amount: float | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListInvoicesResponse200]:
    """List account invoices

     Account-wide invoice list for the authenticated client. The `status` filter mirrors the client
    portal tabs and is a COMPUTED filter (not the raw invoice status column): `open` = not closed and
    billed; `closed` = closed and billed; `past_due` = past the due date and not closed. Readable with a
    read-, operate-, or full-scope customer API key whose permitted areas include this billing area
    (service-scoped keys are not eligible), or with Basic auth + OTP. Internal service-to-service bearer
    tokens are denied on every `/invoices/*` route.

    Args:
        status (ListInvoicesStatus | Unset):  Default: ListInvoicesStatus.OPEN.
        currency (str | Unset):  Example: USD.
        date_due_start (datetime.date | Unset):
        date_due_end (datetime.date | Unset):
        min_amount (float | Unset):
        max_amount (float | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListInvoicesResponse200]
    """

    kwargs = _get_kwargs(
        status=status,
        currency=currency,
        date_due_start=date_due_start,
        date_due_end=date_due_end,
        min_amount=min_amount,
        max_amount=max_amount,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    status: ListInvoicesStatus | Unset = ListInvoicesStatus.OPEN,
    currency: str | Unset = UNSET,
    date_due_start: datetime.date | Unset = UNSET,
    date_due_end: datetime.date | Unset = UNSET,
    min_amount: float | Unset = UNSET,
    max_amount: float | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListInvoicesResponse200 | None:
    """List account invoices

     Account-wide invoice list for the authenticated client. The `status` filter mirrors the client
    portal tabs and is a COMPUTED filter (not the raw invoice status column): `open` = not closed and
    billed; `closed` = closed and billed; `past_due` = past the due date and not closed. Readable with a
    read-, operate-, or full-scope customer API key whose permitted areas include this billing area
    (service-scoped keys are not eligible), or with Basic auth + OTP. Internal service-to-service bearer
    tokens are denied on every `/invoices/*` route.

    Args:
        status (ListInvoicesStatus | Unset):  Default: ListInvoicesStatus.OPEN.
        currency (str | Unset):  Example: USD.
        date_due_start (datetime.date | Unset):
        date_due_end (datetime.date | Unset):
        min_amount (float | Unset):
        max_amount (float | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListInvoicesResponse200
    """

    return sync_detailed(
        client=client,
        status=status,
        currency=currency,
        date_due_start=date_due_start,
        date_due_end=date_due_end,
        min_amount=min_amount,
        max_amount=max_amount,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    status: ListInvoicesStatus | Unset = ListInvoicesStatus.OPEN,
    currency: str | Unset = UNSET,
    date_due_start: datetime.date | Unset = UNSET,
    date_due_end: datetime.date | Unset = UNSET,
    min_amount: float | Unset = UNSET,
    max_amount: float | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListInvoicesResponse200]:
    """List account invoices

     Account-wide invoice list for the authenticated client. The `status` filter mirrors the client
    portal tabs and is a COMPUTED filter (not the raw invoice status column): `open` = not closed and
    billed; `closed` = closed and billed; `past_due` = past the due date and not closed. Readable with a
    read-, operate-, or full-scope customer API key whose permitted areas include this billing area
    (service-scoped keys are not eligible), or with Basic auth + OTP. Internal service-to-service bearer
    tokens are denied on every `/invoices/*` route.

    Args:
        status (ListInvoicesStatus | Unset):  Default: ListInvoicesStatus.OPEN.
        currency (str | Unset):  Example: USD.
        date_due_start (datetime.date | Unset):
        date_due_end (datetime.date | Unset):
        min_amount (float | Unset):
        max_amount (float | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListInvoicesResponse200]
    """

    kwargs = _get_kwargs(
        status=status,
        currency=currency,
        date_due_start=date_due_start,
        date_due_end=date_due_end,
        min_amount=min_amount,
        max_amount=max_amount,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    status: ListInvoicesStatus | Unset = ListInvoicesStatus.OPEN,
    currency: str | Unset = UNSET,
    date_due_start: datetime.date | Unset = UNSET,
    date_due_end: datetime.date | Unset = UNSET,
    min_amount: float | Unset = UNSET,
    max_amount: float | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListInvoicesResponse200 | None:
    """List account invoices

     Account-wide invoice list for the authenticated client. The `status` filter mirrors the client
    portal tabs and is a COMPUTED filter (not the raw invoice status column): `open` = not closed and
    billed; `closed` = closed and billed; `past_due` = past the due date and not closed. Readable with a
    read-, operate-, or full-scope customer API key whose permitted areas include this billing area
    (service-scoped keys are not eligible), or with Basic auth + OTP. Internal service-to-service bearer
    tokens are denied on every `/invoices/*` route.

    Args:
        status (ListInvoicesStatus | Unset):  Default: ListInvoicesStatus.OPEN.
        currency (str | Unset):  Example: USD.
        date_due_start (datetime.date | Unset):
        date_due_end (datetime.date | Unset):
        min_amount (float | Unset):
        max_amount (float | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListInvoicesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            status=status,
            currency=currency,
            date_due_start=date_due_start,
            date_due_end=date_due_end,
            min_amount=min_amount,
            max_amount=max_amount,
            limit=limit,
            offset=offset,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
