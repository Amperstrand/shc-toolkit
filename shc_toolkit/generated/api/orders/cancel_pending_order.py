from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cancel_pending_order_response_200 import CancelPendingOrderResponse200
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    order_id: int,
    *,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/orders/{order_id}/cancel".format(
            order_id=quote(str(order_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CancelPendingOrderResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = CancelPendingOrderResponse200.from_dict(response.json())

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
) -> Response[CancelPendingOrderResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    order_id: int,
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CancelPendingOrderResponse200 | Error]:
    """Cancel an owned pending order that has not yet been fulfilled

     Cancel an authenticated-client-owned pending-fulfillment order. The live /v2 handler accepts no
    request body fields and rejects any supplied key.

    Args:
        order_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelPendingOrderResponse200 | Error]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    order_id: int,
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> CancelPendingOrderResponse200 | Error | None:
    """Cancel an owned pending order that has not yet been fulfilled

     Cancel an authenticated-client-owned pending-fulfillment order. The live /v2 handler accepts no
    request body fields and rejects any supplied key.

    Args:
        order_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelPendingOrderResponse200 | Error
    """

    return sync_detailed(
        order_id=order_id,
        client=client,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    order_id: int,
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CancelPendingOrderResponse200 | Error]:
    """Cancel an owned pending order that has not yet been fulfilled

     Cancel an authenticated-client-owned pending-fulfillment order. The live /v2 handler accepts no
    request body fields and rejects any supplied key.

    Args:
        order_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelPendingOrderResponse200 | Error]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    order_id: int,
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> CancelPendingOrderResponse200 | Error | None:
    """Cancel an owned pending order that has not yet been fulfilled

     Cancel an authenticated-client-owned pending-fulfillment order. The live /v2 handler accepts no
    request body fields and rejects any supplied key.

    Args:
        order_id (int):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelPendingOrderResponse200 | Error
    """

    return (
        await asyncio_detailed(
            order_id=order_id,
            client=client,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
