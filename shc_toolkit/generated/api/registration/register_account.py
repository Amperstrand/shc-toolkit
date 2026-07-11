from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.register_request import RegisterRequest
from ...models.register_response import RegisterResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: RegisterRequest,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/register",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | RegisterResponse | None:
    if response.status_code == 201:
        response_201 = RegisterResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

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
) -> Response[Error | RegisterResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | RegisterResponse]:
    """Create a customer account and receive a usable API key in one anonymous call.

     Anonymous, one-call customer signup. Creates a Blesta client account (the same client-creation path
    as the web order/registration form) and returns a pre-minted, scoped customer API key in the SAME
    201 response, so a developer or AI agent goes from nothing to a usable account plus first API key
    without a second round-trip. No authentication is required (this is the only unauthenticated write
    endpoint documented here; the agent key-bootstrap /agent-keys/claim is the one other public route,
    an internal pairing endpoint). Email is the login identifier (no username). No CAPTCHA, no postal
    address, no phone, no email-verification gate. The new account is INERT until a first order is
    placed and its invoice is paid (registration provisions nothing and costs nothing). This endpoint is
    FRICTIONLESS and is NOT anti-enumeration: if the email is already registered it returns a plain 409
    'email_exists' (this is intentional and accepted). The minted key cannot reach identity/credential
    routes regardless of scope (api-keys, password, 2FA, contact, and the primary-identity PATCH
    /account are Basic+OTP-only for every key). Rate limited per IP (global edge limit plus a tighter
    registration bucket). An optional Idempotency-Key header is honored at the rate-limit level only
    (full replay-storage is deferred for v1; a lost response is recovered by logging in to generate a
    key).

    Args:
        idempotency_key (str | Unset):
        body (RegisterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RegisterResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterRequest,
    idempotency_key: str | Unset = UNSET,
) -> Error | RegisterResponse | None:
    """Create a customer account and receive a usable API key in one anonymous call.

     Anonymous, one-call customer signup. Creates a Blesta client account (the same client-creation path
    as the web order/registration form) and returns a pre-minted, scoped customer API key in the SAME
    201 response, so a developer or AI agent goes from nothing to a usable account plus first API key
    without a second round-trip. No authentication is required (this is the only unauthenticated write
    endpoint documented here; the agent key-bootstrap /agent-keys/claim is the one other public route,
    an internal pairing endpoint). Email is the login identifier (no username). No CAPTCHA, no postal
    address, no phone, no email-verification gate. The new account is INERT until a first order is
    placed and its invoice is paid (registration provisions nothing and costs nothing). This endpoint is
    FRICTIONLESS and is NOT anti-enumeration: if the email is already registered it returns a plain 409
    'email_exists' (this is intentional and accepted). The minted key cannot reach identity/credential
    routes regardless of scope (api-keys, password, 2FA, contact, and the primary-identity PATCH
    /account are Basic+OTP-only for every key). Rate limited per IP (global edge limit plus a tighter
    registration bucket). An optional Idempotency-Key header is honored at the rate-limit level only
    (full replay-storage is deferred for v1; a lost response is recovered by logging in to generate a
    key).

    Args:
        idempotency_key (str | Unset):
        body (RegisterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RegisterResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | RegisterResponse]:
    """Create a customer account and receive a usable API key in one anonymous call.

     Anonymous, one-call customer signup. Creates a Blesta client account (the same client-creation path
    as the web order/registration form) and returns a pre-minted, scoped customer API key in the SAME
    201 response, so a developer or AI agent goes from nothing to a usable account plus first API key
    without a second round-trip. No authentication is required (this is the only unauthenticated write
    endpoint documented here; the agent key-bootstrap /agent-keys/claim is the one other public route,
    an internal pairing endpoint). Email is the login identifier (no username). No CAPTCHA, no postal
    address, no phone, no email-verification gate. The new account is INERT until a first order is
    placed and its invoice is paid (registration provisions nothing and costs nothing). This endpoint is
    FRICTIONLESS and is NOT anti-enumeration: if the email is already registered it returns a plain 409
    'email_exists' (this is intentional and accepted). The minted key cannot reach identity/credential
    routes regardless of scope (api-keys, password, 2FA, contact, and the primary-identity PATCH
    /account are Basic+OTP-only for every key). Rate limited per IP (global edge limit plus a tighter
    registration bucket). An optional Idempotency-Key header is honored at the rate-limit level only
    (full replay-storage is deferred for v1; a lost response is recovered by logging in to generate a
    key).

    Args:
        idempotency_key (str | Unset):
        body (RegisterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RegisterResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterRequest,
    idempotency_key: str | Unset = UNSET,
) -> Error | RegisterResponse | None:
    """Create a customer account and receive a usable API key in one anonymous call.

     Anonymous, one-call customer signup. Creates a Blesta client account (the same client-creation path
    as the web order/registration form) and returns a pre-minted, scoped customer API key in the SAME
    201 response, so a developer or AI agent goes from nothing to a usable account plus first API key
    without a second round-trip. No authentication is required (this is the only unauthenticated write
    endpoint documented here; the agent key-bootstrap /agent-keys/claim is the one other public route,
    an internal pairing endpoint). Email is the login identifier (no username). No CAPTCHA, no postal
    address, no phone, no email-verification gate. The new account is INERT until a first order is
    placed and its invoice is paid (registration provisions nothing and costs nothing). This endpoint is
    FRICTIONLESS and is NOT anti-enumeration: if the email is already registered it returns a plain 409
    'email_exists' (this is intentional and accepted). The minted key cannot reach identity/credential
    routes regardless of scope (api-keys, password, 2FA, contact, and the primary-identity PATCH
    /account are Basic+OTP-only for every key). Rate limited per IP (global edge limit plus a tighter
    registration bucket). An optional Idempotency-Key header is honored at the rate-limit level only
    (full replay-storage is deferred for v1; a lost response is recovered by logging in to generate a
    key).

    Args:
        idempotency_key (str | Unset):
        body (RegisterRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RegisterResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
