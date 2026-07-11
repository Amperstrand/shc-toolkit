from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_quotation_invoices_response_200 import (
    ListQuotationInvoicesResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    quotation_id: int,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/quotations/{quotation_id}/invoices".format(
            quotation_id=quote(str(quotation_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListQuotationInvoicesResponse200 | None:
    if response.status_code == 200:
        response_200 = ListQuotationInvoicesResponse200.from_dict(response.json())

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
) -> Response[Error | ListQuotationInvoicesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    quotation_id: int,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListQuotationInvoicesResponse200]:
    """List invoices generated from a quotation

     Lists the invoices generated from an approved quotation, client-scoped. The invoice status is
    renamed to invoice_status to match the rest of the API.

    Args:
        quotation_id (int):  Example: 9001.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListQuotationInvoicesResponse200]
    """

    kwargs = _get_kwargs(
        quotation_id=quotation_id,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    quotation_id: int,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListQuotationInvoicesResponse200 | None:
    """List invoices generated from a quotation

     Lists the invoices generated from an approved quotation, client-scoped. The invoice status is
    renamed to invoice_status to match the rest of the API.

    Args:
        quotation_id (int):  Example: 9001.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListQuotationInvoicesResponse200
    """

    return sync_detailed(
        quotation_id=quotation_id,
        client=client,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    quotation_id: int,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListQuotationInvoicesResponse200]:
    """List invoices generated from a quotation

     Lists the invoices generated from an approved quotation, client-scoped. The invoice status is
    renamed to invoice_status to match the rest of the API.

    Args:
        quotation_id (int):  Example: 9001.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListQuotationInvoicesResponse200]
    """

    kwargs = _get_kwargs(
        quotation_id=quotation_id,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    quotation_id: int,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListQuotationInvoicesResponse200 | None:
    """List invoices generated from a quotation

     Lists the invoices generated from an approved quotation, client-scoped. The invoice status is
    renamed to invoice_status to match the rest of the API.

    Args:
        quotation_id (int):  Example: 9001.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListQuotationInvoicesResponse200
    """

    return (
        await asyncio_detailed(
            quotation_id=quotation_id,
            client=client,
            limit=limit,
            offset=offset,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
