from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.affiliate_payout_request import AffiliatePayoutRequest
from ...models.error import Error
from ...models.request_affiliate_payout_response_201 import (
    RequestAffiliatePayoutResponse201,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AffiliatePayoutRequest,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/affiliate/payouts",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | RequestAffiliatePayoutResponse201 | None:
    if response.status_code == 201:
        response_201 = RequestAffiliatePayoutResponse201.from_dict(response.json())

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
) -> Response[Error | RequestAffiliatePayoutResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AffiliatePayoutRequest,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | RequestAffiliatePayoutResponse201]:
    """Request an affiliate payout

     Creates a Bitcoin payout REQUEST (status `pending`). This only records the request in Blesta — it
    does NOT send any funds; the actual disbursement is a separate operator process. Mirrors the client
    portal payout request: only one pending request is allowed at a time (`409 conflict` otherwise), the
    requested amount must not exceed the available balance, and it must fall within the affiliate's
    minimum/maximum withdrawal limits (`422 validation_failed` otherwise). Amounts are BTC-native (8
    dp). `requested_currency` is optional and must equal the affiliate withdrawal currency (BTC).
    `payment_method_id` is optional; when only one payout method is configured it is selected
    automatically. Returns `404 not_found` if the client is not enrolled.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (AffiliatePayoutRequest):  Example: {'requested_amount': '0.001',
            'requested_currency': 'BTC'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RequestAffiliatePayoutResponse201]
    """

    kwargs = _get_kwargs(
        body=body,
        limit=limit,
        offset=offset,
        idempotency_key=idempotency_key,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: AffiliatePayoutRequest,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | RequestAffiliatePayoutResponse201 | None:
    """Request an affiliate payout

     Creates a Bitcoin payout REQUEST (status `pending`). This only records the request in Blesta — it
    does NOT send any funds; the actual disbursement is a separate operator process. Mirrors the client
    portal payout request: only one pending request is allowed at a time (`409 conflict` otherwise), the
    requested amount must not exceed the available balance, and it must fall within the affiliate's
    minimum/maximum withdrawal limits (`422 validation_failed` otherwise). Amounts are BTC-native (8
    dp). `requested_currency` is optional and must equal the affiliate withdrawal currency (BTC).
    `payment_method_id` is optional; when only one payout method is configured it is selected
    automatically. Returns `404 not_found` if the client is not enrolled.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (AffiliatePayoutRequest):  Example: {'requested_amount': '0.001',
            'requested_currency': 'BTC'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RequestAffiliatePayoutResponse201
    """

    return sync_detailed(
        client=client,
        body=body,
        limit=limit,
        offset=offset,
        idempotency_key=idempotency_key,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AffiliatePayoutRequest,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | RequestAffiliatePayoutResponse201]:
    """Request an affiliate payout

     Creates a Bitcoin payout REQUEST (status `pending`). This only records the request in Blesta — it
    does NOT send any funds; the actual disbursement is a separate operator process. Mirrors the client
    portal payout request: only one pending request is allowed at a time (`409 conflict` otherwise), the
    requested amount must not exceed the available balance, and it must fall within the affiliate's
    minimum/maximum withdrawal limits (`422 validation_failed` otherwise). Amounts are BTC-native (8
    dp). `requested_currency` is optional and must equal the affiliate withdrawal currency (BTC).
    `payment_method_id` is optional; when only one payout method is configured it is selected
    automatically. Returns `404 not_found` if the client is not enrolled.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (AffiliatePayoutRequest):  Example: {'requested_amount': '0.001',
            'requested_currency': 'BTC'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RequestAffiliatePayoutResponse201]
    """

    kwargs = _get_kwargs(
        body=body,
        limit=limit,
        offset=offset,
        idempotency_key=idempotency_key,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AffiliatePayoutRequest,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | RequestAffiliatePayoutResponse201 | None:
    """Request an affiliate payout

     Creates a Bitcoin payout REQUEST (status `pending`). This only records the request in Blesta — it
    does NOT send any funds; the actual disbursement is a separate operator process. Mirrors the client
    portal payout request: only one pending request is allowed at a time (`409 conflict` otherwise), the
    requested amount must not exceed the available balance, and it must fall within the affiliate's
    minimum/maximum withdrawal limits (`422 validation_failed` otherwise). Amounts are BTC-native (8
    dp). `requested_currency` is optional and must equal the affiliate withdrawal currency (BTC).
    `payment_method_id` is optional; when only one payout method is configured it is selected
    automatically. Returns `404 not_found` if the client is not enrolled.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (AffiliatePayoutRequest):  Example: {'requested_amount': '0.001',
            'requested_currency': 'BTC'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RequestAffiliatePayoutResponse201
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            limit=limit,
            offset=offset,
            idempotency_key=idempotency_key,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
