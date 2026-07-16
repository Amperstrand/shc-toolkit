from http import HTTPStatus
from io import BytesIO
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    invoice_id: int,
    *,
    format_: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/invoices/{invoice_id}/electronic".format(
            invoice_id=quote(str(invoice_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | File | None:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    invoice_id: int,
    *,
    client: AuthenticatedClient | Client,
    format_: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | File]:
    """Download the electronic representation of an owned invoice (binary)

     Download an electronic invoice document for an authenticated-client-owned invoice.

    Args:
        invoice_id (int):
        format_ (str | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | File]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
        format_=format_,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    invoice_id: int,
    *,
    client: AuthenticatedClient | Client,
    format_: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | File | None:
    """Download the electronic representation of an owned invoice (binary)

     Download an electronic invoice document for an authenticated-client-owned invoice.

    Args:
        invoice_id (int):
        format_ (str | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | File
    """

    return sync_detailed(
        invoice_id=invoice_id,
        client=client,
        format_=format_,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    invoice_id: int,
    *,
    client: AuthenticatedClient | Client,
    format_: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | File]:
    """Download the electronic representation of an owned invoice (binary)

     Download an electronic invoice document for an authenticated-client-owned invoice.

    Args:
        invoice_id (int):
        format_ (str | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | File]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
        format_=format_,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    invoice_id: int,
    *,
    client: AuthenticatedClient | Client,
    format_: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | File | None:
    """Download the electronic representation of an owned invoice (binary)

     Download an electronic invoice document for an authenticated-client-owned invoice.

    Args:
        invoice_id (int):
        format_ (str | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | File
    """

    return (
        await asyncio_detailed(
            invoice_id=invoice_id,
            client=client,
            format_=format_,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
