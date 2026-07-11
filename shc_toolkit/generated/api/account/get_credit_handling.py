from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_credit_handling_response_200 import GetCreditHandlingResponse200
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
        "url": "/account/credit-handling",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetCreditHandlingResponse200 | None:
    if response.status_code == 200:
        response_200 = GetCreditHandlingResponse200.from_dict(response.json())

        return response_200

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
) -> Response[Error | GetCreditHandlingResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetCreditHandlingResponse200]:
    """Get low-credit auto-recharge thresholds

     Returns the per-currency low-credit thresholds used for auto-debit recharge, plus whether account
    credit is enabled for this company. Thresholds are normalized to 4 decimal places.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetCreditHandlingResponse200]
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
    client: AuthenticatedClient,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetCreditHandlingResponse200 | None:
    """Get low-credit auto-recharge thresholds

     Returns the per-currency low-credit thresholds used for auto-debit recharge, plus whether account
    credit is enabled for this company. Thresholds are normalized to 4 decimal places.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetCreditHandlingResponse200
    """

    return sync_detailed(
        client=client,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | GetCreditHandlingResponse200]:
    """Get low-credit auto-recharge thresholds

     Returns the per-currency low-credit thresholds used for auto-debit recharge, plus whether account
    credit is enabled for this company. Thresholds are normalized to 4 decimal places.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetCreditHandlingResponse200]
    """

    kwargs = _get_kwargs(
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | GetCreditHandlingResponse200 | None:
    """Get low-credit auto-recharge thresholds

     Returns the per-currency low-credit thresholds used for auto-debit recharge, plus whether account
    credit is enabled for this company. Thresholds are normalized to 4 decimal places.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetCreditHandlingResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
