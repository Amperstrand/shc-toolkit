from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.enable_two_factor_body import EnableTwoFactorBody
from ...models.enable_two_factor_response_200 import EnableTwoFactorResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: EnableTwoFactorBody,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/account/2fa",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EnableTwoFactorResponse200 | None:
    if response.status_code == 200:
        response_200 = EnableTwoFactorResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[EnableTwoFactorResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: EnableTwoFactorBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[EnableTwoFactorResponse200]:
    """Enable two-factor authentication

     Enables TOTP two-factor for the account. Requires the current password and a valid code for the key
    returned by POST /account/2fa/enrollment. Requires Basic+OTP front-door authentication; not
    available to API keys or agent sessions.

    Args:
        x_user_api_otp (str | Unset):
        body (EnableTwoFactorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnableTwoFactorResponse200]
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
    client: AuthenticatedClient | Client,
    body: EnableTwoFactorBody,
    x_user_api_otp: str | Unset = UNSET,
) -> EnableTwoFactorResponse200 | None:
    """Enable two-factor authentication

     Enables TOTP two-factor for the account. Requires the current password and a valid code for the key
    returned by POST /account/2fa/enrollment. Requires Basic+OTP front-door authentication; not
    available to API keys or agent sessions.

    Args:
        x_user_api_otp (str | Unset):
        body (EnableTwoFactorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnableTwoFactorResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: EnableTwoFactorBody,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[EnableTwoFactorResponse200]:
    """Enable two-factor authentication

     Enables TOTP two-factor for the account. Requires the current password and a valid code for the key
    returned by POST /account/2fa/enrollment. Requires Basic+OTP front-door authentication; not
    available to API keys or agent sessions.

    Args:
        x_user_api_otp (str | Unset):
        body (EnableTwoFactorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnableTwoFactorResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: EnableTwoFactorBody,
    x_user_api_otp: str | Unset = UNSET,
) -> EnableTwoFactorResponse200 | None:
    """Enable two-factor authentication

     Enables TOTP two-factor for the account. Requires the current password and a valid code for the key
    returned by POST /account/2fa/enrollment. Requires Basic+OTP front-door authentication; not
    available to API keys or agent sessions.

    Args:
        x_user_api_otp (str | Unset):
        body (EnableTwoFactorBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnableTwoFactorResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
