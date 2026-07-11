from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    invoice_id: int,
    *,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/invoices/{invoice_id}/pdf".format(
            invoice_id=quote(str(invoice_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | None:
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

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
) -> Response[Error]:
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
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error]:
    r"""Download invoice PDF

     Downloads the authenticated client's own invoice as a PDF document. The invoice is rendered server-
    side (TCPDF) and streamed as a binary `application/pdf` attachment — this is a binary download,
    **not** the standard JSON `{ \"data\": ... }` envelope returned by the other endpoints. Ownership is
    enforced at the SQL layer (`WHERE i.id = ? AND i.client_id = ?`) before any byte is emitted.
    Reachable with a read-, operate-, or full-scope customer API key whose permitted areas include
    billing (service-scoped keys are not eligible), or with HTTP Basic (plus `X-User-Api-OTP` when 2FA
    is enabled). Internal service-to-service bearer tokens are denied on every `/invoices/*` route
    (403/401 per the bearer audience gate). This endpoint has its own per-client+invoice+IP rate-limit
    bucket to bound the server-side render cost independent of the global request cap.

    Args:
        invoice_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
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
    x_user_api_otp: str | Unset = UNSET,
) -> Error | None:
    r"""Download invoice PDF

     Downloads the authenticated client's own invoice as a PDF document. The invoice is rendered server-
    side (TCPDF) and streamed as a binary `application/pdf` attachment — this is a binary download,
    **not** the standard JSON `{ \"data\": ... }` envelope returned by the other endpoints. Ownership is
    enforced at the SQL layer (`WHERE i.id = ? AND i.client_id = ?`) before any byte is emitted.
    Reachable with a read-, operate-, or full-scope customer API key whose permitted areas include
    billing (service-scoped keys are not eligible), or with HTTP Basic (plus `X-User-Api-OTP` when 2FA
    is enabled). Internal service-to-service bearer tokens are denied on every `/invoices/*` route
    (403/401 per the bearer audience gate). This endpoint has its own per-client+invoice+IP rate-limit
    bucket to bound the server-side render cost independent of the global request cap.

    Args:
        invoice_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
    """

    return sync_detailed(
        invoice_id=invoice_id,
        client=client,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    invoice_id: int,
    *,
    client: AuthenticatedClient,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error]:
    r"""Download invoice PDF

     Downloads the authenticated client's own invoice as a PDF document. The invoice is rendered server-
    side (TCPDF) and streamed as a binary `application/pdf` attachment — this is a binary download,
    **not** the standard JSON `{ \"data\": ... }` envelope returned by the other endpoints. Ownership is
    enforced at the SQL layer (`WHERE i.id = ? AND i.client_id = ?`) before any byte is emitted.
    Reachable with a read-, operate-, or full-scope customer API key whose permitted areas include
    billing (service-scoped keys are not eligible), or with HTTP Basic (plus `X-User-Api-OTP` when 2FA
    is enabled). Internal service-to-service bearer tokens are denied on every `/invoices/*` route
    (403/401 per the bearer audience gate). This endpoint has its own per-client+invoice+IP rate-limit
    bucket to bound the server-side render cost independent of the global request cap.

    Args:
        invoice_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
    """

    kwargs = _get_kwargs(
        invoice_id=invoice_id,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    invoice_id: int,
    *,
    client: AuthenticatedClient,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | None:
    r"""Download invoice PDF

     Downloads the authenticated client's own invoice as a PDF document. The invoice is rendered server-
    side (TCPDF) and streamed as a binary `application/pdf` attachment — this is a binary download,
    **not** the standard JSON `{ \"data\": ... }` envelope returned by the other endpoints. Ownership is
    enforced at the SQL layer (`WHERE i.id = ? AND i.client_id = ?`) before any byte is emitted.
    Reachable with a read-, operate-, or full-scope customer API key whose permitted areas include
    billing (service-scoped keys are not eligible), or with HTTP Basic (plus `X-User-Api-OTP` when 2FA
    is enabled). Internal service-to-service bearer tokens are denied on every `/invoices/*` route
    (403/401 per the bearer audience gate). This endpoint has its own per-client+invoice+IP rate-limit
    bucket to bound the server-side render cost independent of the global request cap.

    Args:
        invoice_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
    """

    return (
        await asyncio_detailed(
            invoice_id=invoice_id,
            client=client,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
