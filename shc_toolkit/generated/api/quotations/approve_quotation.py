from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.approve_quotation_body import ApproveQuotationBody
from ...models.approve_quotation_response_201 import ApproveQuotationResponse201
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    quotation_id: int,
    *,
    body: ApproveQuotationBody,
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
        "url": "/quotations/{quotation_id}/approve".format(
            quotation_id=quote(str(quotation_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApproveQuotationResponse201 | Error | None:
    if response.status_code == 201:
        response_201 = ApproveQuotationResponse201.from_dict(response.json())

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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

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
) -> Response[ApproveQuotationResponse201 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    quotation_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ApproveQuotationBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[ApproveQuotationResponse201 | Error]:
    """Approve an owned quotation and create the resulting invoice or checkout pointer

     Approve an authenticated-client-owned pending quotation using the live /v2 quotation_id path and
    body idempotency_key.

    Args:
        quotation_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (ApproveQuotationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApproveQuotationResponse201 | Error]
    """

    kwargs = _get_kwargs(
        quotation_id=quotation_id,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    quotation_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ApproveQuotationBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> ApproveQuotationResponse201 | Error | None:
    """Approve an owned quotation and create the resulting invoice or checkout pointer

     Approve an authenticated-client-owned pending quotation using the live /v2 quotation_id path and
    body idempotency_key.

    Args:
        quotation_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (ApproveQuotationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApproveQuotationResponse201 | Error
    """

    return sync_detailed(
        quotation_id=quotation_id,
        client=client,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    quotation_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ApproveQuotationBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[ApproveQuotationResponse201 | Error]:
    """Approve an owned quotation and create the resulting invoice or checkout pointer

     Approve an authenticated-client-owned pending quotation using the live /v2 quotation_id path and
    body idempotency_key.

    Args:
        quotation_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (ApproveQuotationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApproveQuotationResponse201 | Error]
    """

    kwargs = _get_kwargs(
        quotation_id=quotation_id,
        body=body,
        x_user_api_confirm=x_user_api_confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    quotation_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: ApproveQuotationBody,
    x_user_api_confirm: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> ApproveQuotationResponse201 | Error | None:
    """Approve an owned quotation and create the resulting invoice or checkout pointer

     Approve an authenticated-client-owned pending quotation using the live /v2 quotation_id path and
    body idempotency_key.

    Args:
        quotation_id (int):
        x_user_api_confirm (str | Unset):
        x_user_api_otp (str | Unset):
        body (ApproveQuotationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApproveQuotationResponse201 | Error
    """

    return (
        await asyncio_detailed(
            quotation_id=quotation_id,
            client=client,
            body=body,
            x_user_api_confirm=x_user_api_confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
