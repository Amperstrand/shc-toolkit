from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.update_account_contact_request import UpdateAccountContactRequest
from ...models.update_account_contact_response_200 import (
    UpdateAccountContactResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: UpdateAccountContactRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/account/contact",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UpdateAccountContactResponse200 | None:
    if response.status_code == 200:
        response_200 = UpdateAccountContactResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 405:
        response_405 = Error.from_dict(response.json())

        return response_405

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
) -> Response[Error | UpdateAccountContactResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: UpdateAccountContactRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateAccountContactResponse200]:
    """Update primary contact profile

     Updates the authenticated customer's primary contact record. Send only the fields you want to
    change. If the email address changes, the API forces Blesta's email-verification flow for the
    updated address.

    Args:
        x_user_api_otp (str | Unset):
        body (UpdateAccountContactRequest): Apply any subset of the supported primary-contact
            fields. At least one field must be supplied; empty-string values are rejected on the
            supplied fields. If `phone` is supplied, use E.164 formatting when possible. Example:
            {'email': 'billing@example.com', 'phone': '+15125550123', 'address1': '200 Congress Ave',
            'city': 'Austin', 'state': 'TX', 'zip': '78701', 'country': 'US'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateAccountContactResponse200]
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
    body: UpdateAccountContactRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateAccountContactResponse200 | None:
    """Update primary contact profile

     Updates the authenticated customer's primary contact record. Send only the fields you want to
    change. If the email address changes, the API forces Blesta's email-verification flow for the
    updated address.

    Args:
        x_user_api_otp (str | Unset):
        body (UpdateAccountContactRequest): Apply any subset of the supported primary-contact
            fields. At least one field must be supplied; empty-string values are rejected on the
            supplied fields. If `phone` is supplied, use E.164 formatting when possible. Example:
            {'email': 'billing@example.com', 'phone': '+15125550123', 'address1': '200 Congress Ave',
            'city': 'Austin', 'state': 'TX', 'zip': '78701', 'country': 'US'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateAccountContactResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: UpdateAccountContactRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateAccountContactResponse200]:
    """Update primary contact profile

     Updates the authenticated customer's primary contact record. Send only the fields you want to
    change. If the email address changes, the API forces Blesta's email-verification flow for the
    updated address.

    Args:
        x_user_api_otp (str | Unset):
        body (UpdateAccountContactRequest): Apply any subset of the supported primary-contact
            fields. At least one field must be supplied; empty-string values are rejected on the
            supplied fields. If `phone` is supplied, use E.164 formatting when possible. Example:
            {'email': 'billing@example.com', 'phone': '+15125550123', 'address1': '200 Congress Ave',
            'city': 'Austin', 'state': 'TX', 'zip': '78701', 'country': 'US'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateAccountContactResponse200]
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
    body: UpdateAccountContactRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateAccountContactResponse200 | None:
    """Update primary contact profile

     Updates the authenticated customer's primary contact record. Send only the fields you want to
    change. If the email address changes, the API forces Blesta's email-verification flow for the
    updated address.

    Args:
        x_user_api_otp (str | Unset):
        body (UpdateAccountContactRequest): Apply any subset of the supported primary-contact
            fields. At least one field must be supplied; empty-string values are rejected on the
            supplied fields. If `phone` is supplied, use E.164 formatting when possible. Example:
            {'email': 'billing@example.com', 'phone': '+15125550123', 'address1': '200 Congress Ave',
            'city': 'Austin', 'state': 'TX', 'zip': '78701', 'country': 'US'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateAccountContactResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
