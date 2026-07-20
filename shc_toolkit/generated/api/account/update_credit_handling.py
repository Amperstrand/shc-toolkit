from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.credit_handling_update_request import CreditHandlingUpdateRequest
from ...models.error import Error
from ...models.update_credit_handling_response_200 import (
    UpdateCreditHandlingResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CreditHandlingUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/account/credit-handling",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UpdateCreditHandlingResponse200 | None:
    if response.status_code == 200:
        response_200 = UpdateCreditHandlingResponse200.from_dict(response.json())

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
) -> Response[Error | UpdateCreditHandlingResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreditHandlingUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateCreditHandlingResponse200]:
    """Replace credit-handling thresholds

     Full replacement of the per-currency low-credit notification threshold map. Disabled when the
    company turns off credit handling (403). Returns the refreshed credit-handling settings.

    Args:
        x_user_api_otp (str | Unset):
        body (CreditHandlingUpdateRequest): Full replacement of the per-currency low-credit
            notification threshold map. An empty `thresholds` object clears all thresholds. Example:
            {'thresholds': {'USD': '10.00'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateCreditHandlingResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreditHandlingUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateCreditHandlingResponse200 | None:
    """Replace credit-handling thresholds

     Full replacement of the per-currency low-credit notification threshold map. Disabled when the
    company turns off credit handling (403). Returns the refreshed credit-handling settings.

    Args:
        x_user_api_otp (str | Unset):
        body (CreditHandlingUpdateRequest): Full replacement of the per-currency low-credit
            notification threshold map. An empty `thresholds` object clears all thresholds. Example:
            {'thresholds': {'USD': '10.00'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateCreditHandlingResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreditHandlingUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateCreditHandlingResponse200]:
    """Replace credit-handling thresholds

     Full replacement of the per-currency low-credit notification threshold map. Disabled when the
    company turns off credit handling (403). Returns the refreshed credit-handling settings.

    Args:
        x_user_api_otp (str | Unset):
        body (CreditHandlingUpdateRequest): Full replacement of the per-currency low-credit
            notification threshold map. An empty `thresholds` object clears all thresholds. Example:
            {'thresholds': {'USD': '10.00'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateCreditHandlingResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreditHandlingUpdateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateCreditHandlingResponse200 | None:
    """Replace credit-handling thresholds

     Full replacement of the per-currency low-credit notification threshold map. Disabled when the
    company turns off credit handling (403). Returns the refreshed credit-handling settings.

    Args:
        x_user_api_otp (str | Unset):
        body (CreditHandlingUpdateRequest): Full replacement of the per-currency low-credit
            notification threshold map. An empty `thresholds` object clears all thresholds. Example:
            {'thresholds': {'USD': '10.00'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateCreditHandlingResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
