from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.enroll_affiliate_response_201 import EnrollAffiliateResponse201
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/affiliate/enroll",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EnrollAffiliateResponse201 | Error | None:
    if response.status_code == 201:
        response_201 = EnrollAffiliateResponse201.from_dict(response.json())

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
) -> Response[EnrollAffiliateResponse201 | Error]:
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
) -> Response[EnrollAffiliateResponse201 | Error]:
    """Enroll the account as an affiliate

     Enrolls the authenticated client in the affiliate program and auto-approves it (status `active`),
    exactly as the client portal signup does. The program is restricted to current customers: the client
    must have at least one `active` service, otherwise the call returns `403 forbidden`. If the account
    is already enrolled the call returns `409 conflict`. On success returns the same payload as `GET
    /affiliate`. Takes no request body.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnrollAffiliateResponse201 | Error]
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
) -> EnrollAffiliateResponse201 | Error | None:
    """Enroll the account as an affiliate

     Enrolls the authenticated client in the affiliate program and auto-approves it (status `active`),
    exactly as the client portal signup does. The program is restricted to current customers: the client
    must have at least one `active` service, otherwise the call returns `403 forbidden`. If the account
    is already enrolled the call returns `409 conflict`. On success returns the same payload as `GET
    /affiliate`. Takes no request body.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnrollAffiliateResponse201 | Error
    """

    return sync_detailed(
        client=client,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[EnrollAffiliateResponse201 | Error]:
    """Enroll the account as an affiliate

     Enrolls the authenticated client in the affiliate program and auto-approves it (status `active`),
    exactly as the client portal signup does. The program is restricted to current customers: the client
    must have at least one `active` service, otherwise the call returns `403 forbidden`. If the account
    is already enrolled the call returns `409 conflict`. On success returns the same payload as `GET
    /affiliate`. Takes no request body.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnrollAffiliateResponse201 | Error]
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
) -> EnrollAffiliateResponse201 | Error | None:
    """Enroll the account as an affiliate

     Enrolls the authenticated client in the affiliate program and auto-approves it (status `active`),
    exactly as the client portal signup does. The program is restricted to current customers: the client
    must have at least one `active` service, otherwise the call returns `403 forbidden`. If the account
    is already enrolled the call returns `409 conflict`. On success returns the same payload as `GET
    /affiliate`. Takes no request body.

    Args:
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnrollAffiliateResponse201 | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
