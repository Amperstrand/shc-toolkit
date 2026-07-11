from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_invoice_response_200 import GetInvoiceResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    invoice_id: int,
    *,
    line_items_limit: int | Unset = 100,
    line_items_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["line_items.limit"] = line_items_limit

    params["line_items.offset"] = line_items_offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/invoices/{invoice_id}".format(
            invoice_id=quote(str(invoice_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetInvoiceResponse200 | None:
    if response.status_code == 200:
        response_200 = GetInvoiceResponse200.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | GetInvoiceResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    invoice_id: int,
    *,
    client: AuthenticatedClient,
    line_items_limit: int | Unset = 100,
    line_items_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetInvoiceResponse200]:
    """Get invoice detail

     Single invoice with paginated line items. When the `inv_display_payments` company setting is
    enabled, an `applied_payments` array of the transactions applied to the invoice is included (omitted
    otherwise, matching the portal). Ownership is enforced at the SQL layer before any applied-payment
    join.

    Args:
        invoice_id (int):
        line_items_limit (int | Unset):  Default: 100.
        line_items_offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetInvoiceResponse200]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
        line_items_limit=line_items_limit,
        line_items_offset=line_items_offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    invoice_id: int,
    *,
    client: AuthenticatedClient,
    line_items_limit: int | Unset = 100,
    line_items_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetInvoiceResponse200 | None:
    """Get invoice detail

     Single invoice with paginated line items. When the `inv_display_payments` company setting is
    enabled, an `applied_payments` array of the transactions applied to the invoice is included (omitted
    otherwise, matching the portal). Ownership is enforced at the SQL layer before any applied-payment
    join.

    Args:
        invoice_id (int):
        line_items_limit (int | Unset):  Default: 100.
        line_items_offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetInvoiceResponse200
    """

    return sync_detailed(
        invoice_id=invoice_id,
        client=client,
        line_items_limit=line_items_limit,
        line_items_offset=line_items_offset,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    invoice_id: int,
    *,
    client: AuthenticatedClient,
    line_items_limit: int | Unset = 100,
    line_items_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetInvoiceResponse200]:
    """Get invoice detail

     Single invoice with paginated line items. When the `inv_display_payments` company setting is
    enabled, an `applied_payments` array of the transactions applied to the invoice is included (omitted
    otherwise, matching the portal). Ownership is enforced at the SQL layer before any applied-payment
    join.

    Args:
        invoice_id (int):
        line_items_limit (int | Unset):  Default: 100.
        line_items_offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetInvoiceResponse200]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
        line_items_limit=line_items_limit,
        line_items_offset=line_items_offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    invoice_id: int,
    *,
    client: AuthenticatedClient,
    line_items_limit: int | Unset = 100,
    line_items_offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetInvoiceResponse200 | None:
    """Get invoice detail

     Single invoice with paginated line items. When the `inv_display_payments` company setting is
    enabled, an `applied_payments` array of the transactions applied to the invoice is included (omitted
    otherwise, matching the portal). Ownership is enforced at the SQL layer before any applied-payment
    join.

    Args:
        invoice_id (int):
        line_items_limit (int | Unset):  Default: 100.
        line_items_offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetInvoiceResponse200
    """

    return (
        await asyncio_detailed(
            invoice_id=invoice_id,
            client=client,
            line_items_limit=line_items_limit,
            line_items_offset=line_items_offset,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
