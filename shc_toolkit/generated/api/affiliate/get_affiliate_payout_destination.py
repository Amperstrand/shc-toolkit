from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_affiliate_payout_destination_response_200 import (
    GetAffiliatePayoutDestinationResponse200,
)
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
        "url": "/affiliate/payout-destination",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetAffiliatePayoutDestinationResponse200 | None:
    if response.status_code == 200:
        response_200 = GetAffiliatePayoutDestinationResponse200.from_dict(
            response.json()
        )

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
) -> Response[Error | GetAffiliatePayoutDestinationResponse200]:
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
) -> Response[Error | GetAffiliatePayoutDestinationResponse200]:
    """Get the affiliate payout destination

     Returns the on-chain and Lightning Bitcoin payout destinations stored for the authenticated client's
    affiliate. Either field is `null` when unset. Returns `404 not_found` if the client is not enrolled.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetAffiliatePayoutDestinationResponse200]
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
) -> Error | GetAffiliatePayoutDestinationResponse200 | None:
    """Get the affiliate payout destination

     Returns the on-chain and Lightning Bitcoin payout destinations stored for the authenticated client's
    affiliate. Either field is `null` when unset. Returns `404 not_found` if the client is not enrolled.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetAffiliatePayoutDestinationResponse200
    """

    return sync_detailed(
        client=client,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetAffiliatePayoutDestinationResponse200]:
    """Get the affiliate payout destination

     Returns the on-chain and Lightning Bitcoin payout destinations stored for the authenticated client's
    affiliate. Either field is `null` when unset. Returns `404 not_found` if the client is not enrolled.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetAffiliatePayoutDestinationResponse200]
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
) -> Error | GetAffiliatePayoutDestinationResponse200 | None:
    """Get the affiliate payout destination

     Returns the on-chain and Lightning Bitcoin payout destinations stored for the authenticated client's
    affiliate. Either field is `null` when unset. Returns `404 not_found` if the client is not enrolled.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetAffiliatePayoutDestinationResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
