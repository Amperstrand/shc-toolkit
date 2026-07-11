from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.contact_create_request import ContactCreateRequest
from ...models.create_contact_response_201 import CreateContactResponse201
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ContactCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/contacts",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateContactResponse201 | Error | None:
    if response.status_code == 201:
        response_201 = CreateContactResponse201.from_dict(response.json())

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
) -> Response[CreateContactResponse201 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ContactCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CreateContactResponse201 | Error]:
    """Create a contact

     Creates a new client-owned contact (parity with the portal add-contact flow). `contact_type` is a
    non-primary type (`billing` or `other`, or a numeric custom contact-type id; a numeric id is stored
    as type `other`). Optionally grants permission areas (from GET /contacts/permission-options),
    attaches a single E.164 phone number, and enables a portal login for the contact. Client-group
    required-contact-fields and email format are enforced server-side. The account primary contact is
    managed via PATCH /account/contact, not here.

    Args:
        x_user_api_otp (str | Unset):
        body (ContactCreateRequest): Fields for creating a client-owned contact. Mirrors the
            portal add-contact form. Example: {'first_name': 'Jane', 'last_name': 'Roe', 'email':
            'jane.roe@example.com', 'contact_type': 'billing'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateContactResponse201 | Error]
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
    body: ContactCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> CreateContactResponse201 | Error | None:
    """Create a contact

     Creates a new client-owned contact (parity with the portal add-contact flow). `contact_type` is a
    non-primary type (`billing` or `other`, or a numeric custom contact-type id; a numeric id is stored
    as type `other`). Optionally grants permission areas (from GET /contacts/permission-options),
    attaches a single E.164 phone number, and enables a portal login for the contact. Client-group
    required-contact-fields and email format are enforced server-side. The account primary contact is
    managed via PATCH /account/contact, not here.

    Args:
        x_user_api_otp (str | Unset):
        body (ContactCreateRequest): Fields for creating a client-owned contact. Mirrors the
            portal add-contact form. Example: {'first_name': 'Jane', 'last_name': 'Roe', 'email':
            'jane.roe@example.com', 'contact_type': 'billing'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateContactResponse201 | Error
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ContactCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[CreateContactResponse201 | Error]:
    """Create a contact

     Creates a new client-owned contact (parity with the portal add-contact flow). `contact_type` is a
    non-primary type (`billing` or `other`, or a numeric custom contact-type id; a numeric id is stored
    as type `other`). Optionally grants permission areas (from GET /contacts/permission-options),
    attaches a single E.164 phone number, and enables a portal login for the contact. Client-group
    required-contact-fields and email format are enforced server-side. The account primary contact is
    managed via PATCH /account/contact, not here.

    Args:
        x_user_api_otp (str | Unset):
        body (ContactCreateRequest): Fields for creating a client-owned contact. Mirrors the
            portal add-contact form. Example: {'first_name': 'Jane', 'last_name': 'Roe', 'email':
            'jane.roe@example.com', 'contact_type': 'billing'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateContactResponse201 | Error]
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
    body: ContactCreateRequest,
    x_user_api_otp: str | Unset = UNSET,
) -> CreateContactResponse201 | Error | None:
    """Create a contact

     Creates a new client-owned contact (parity with the portal add-contact flow). `contact_type` is a
    non-primary type (`billing` or `other`, or a numeric custom contact-type id; a numeric id is stored
    as type `other`). Optionally grants permission areas (from GET /contacts/permission-options),
    attaches a single E.164 phone number, and enables a portal login for the contact. Client-group
    required-contact-fields and email format are enforced server-side. The account primary contact is
    managed via PATCH /account/contact, not here.

    Args:
        x_user_api_otp (str | Unset):
        body (ContactCreateRequest): Fields for creating a client-owned contact. Mirrors the
            portal add-contact form. Example: {'first_name': 'Jane', 'last_name': 'Roe', 'email':
            'jane.roe@example.com', 'contact_type': 'billing'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateContactResponse201 | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
