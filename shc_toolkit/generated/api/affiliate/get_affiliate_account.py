from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_affiliate_account_response_200 import GetAffiliateAccountResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/affiliate",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetAffiliateAccountResponse200 | None:
    if response.status_code == 200:
        response_200 = GetAffiliateAccountResponse200.from_dict(response.json())

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
) -> Response[Error | GetAffiliateAccountResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetAffiliateAccountResponse200]:
    r"""Get the affiliate account overview

     Returns the authenticated client's affiliate account: status, referral code and full referral link,
    lifetime stats (visits, sales, conversion rate), available Bitcoin balance, and the program terms
    (commission, withdrawal limits, cookie window). If the client is not enrolled, returns `{
    \"enrolled\": false, \"status\": \"not_enrolled\", \"eligible\": <bool>, \"program\": {...} }` where
    `eligible` reflects the same active-service gate that `POST /affiliate/enroll` enforces. Self-
    scoped: the affiliate is resolved strictly from the authenticated client; no other affiliate is ever
    visible. Reports figures only; moves no money. Balances are BTC-native (8 decimal places); the BTC
    figures are not run through Blesta's FX layer.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetAffiliateAccountResponse200]
    """

    kwargs = _get_kwargs(
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetAffiliateAccountResponse200 | None:
    r"""Get the affiliate account overview

     Returns the authenticated client's affiliate account: status, referral code and full referral link,
    lifetime stats (visits, sales, conversion rate), available Bitcoin balance, and the program terms
    (commission, withdrawal limits, cookie window). If the client is not enrolled, returns `{
    \"enrolled\": false, \"status\": \"not_enrolled\", \"eligible\": <bool>, \"program\": {...} }` where
    `eligible` reflects the same active-service gate that `POST /affiliate/enroll` enforces. Self-
    scoped: the affiliate is resolved strictly from the authenticated client; no other affiliate is ever
    visible. Reports figures only; moves no money. Balances are BTC-native (8 decimal places); the BTC
    figures are not run through Blesta's FX layer.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetAffiliateAccountResponse200
    """

    return sync_detailed(
        client=client,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetAffiliateAccountResponse200]:
    r"""Get the affiliate account overview

     Returns the authenticated client's affiliate account: status, referral code and full referral link,
    lifetime stats (visits, sales, conversion rate), available Bitcoin balance, and the program terms
    (commission, withdrawal limits, cookie window). If the client is not enrolled, returns `{
    \"enrolled\": false, \"status\": \"not_enrolled\", \"eligible\": <bool>, \"program\": {...} }` where
    `eligible` reflects the same active-service gate that `POST /affiliate/enroll` enforces. Self-
    scoped: the affiliate is resolved strictly from the authenticated client; no other affiliate is ever
    visible. Reports figures only; moves no money. Balances are BTC-native (8 decimal places); the BTC
    figures are not run through Blesta's FX layer.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetAffiliateAccountResponse200]
    """

    kwargs = _get_kwargs(
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetAffiliateAccountResponse200 | None:
    r"""Get the affiliate account overview

     Returns the authenticated client's affiliate account: status, referral code and full referral link,
    lifetime stats (visits, sales, conversion rate), available Bitcoin balance, and the program terms
    (commission, withdrawal limits, cookie window). If the client is not enrolled, returns `{
    \"enrolled\": false, \"status\": \"not_enrolled\", \"eligible\": <bool>, \"program\": {...} }` where
    `eligible` reflects the same active-service gate that `POST /affiliate/enroll` enforces. Self-
    scoped: the affiliate is resolved strictly from the authenticated client; no other affiliate is ever
    visible. Reports figures only; moves no money. Balances are BTC-native (8 decimal places); the BTC
    figures are not run through Blesta's FX layer.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetAffiliateAccountResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
