from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_contact_response_200 import DeleteContactResponse200
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    contact_id: int,
    *,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["confirm"] = confirm

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/contacts/{contact_id}".format(
            contact_id=quote(str(contact_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteContactResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = DeleteContactResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 405:
        response_405 = Error.from_dict(response.json())

        return response_405

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

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
) -> Response[DeleteContactResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    contact_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteContactResponse200 | Error]:
    """Delete a contact

     Deletes one of the authenticated client's additional contacts. The primary contact cannot be deleted
    (409). 404 existence-hiding for foreign/missing contacts.

    Args:
        contact_id (int):  Example: 88.
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteContactResponse200 | Error]
    """

    kwargs = _get_kwargs(
        contact_id=contact_id,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    contact_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteContactResponse200 | Error | None:
    """Delete a contact

     Deletes one of the authenticated client's additional contacts. The primary contact cannot be deleted
    (409). 404 existence-hiding for foreign/missing contacts.

    Args:
        contact_id (int):  Example: 88.
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteContactResponse200 | Error
    """

    return sync_detailed(
        contact_id=contact_id,
        client=client,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    contact_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[DeleteContactResponse200 | Error]:
    """Delete a contact

     Deletes one of the authenticated client's additional contacts. The primary contact cannot be deleted
    (409). 404 existence-hiding for foreign/missing contacts.

    Args:
        contact_id (int):  Example: 88.
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteContactResponse200 | Error]
    """

    kwargs = _get_kwargs(
        contact_id=contact_id,
        confirm=confirm,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    contact_id: int,
    *,
    client: AuthenticatedClient,
    confirm: bool | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> DeleteContactResponse200 | Error | None:
    """Delete a contact

     Deletes one of the authenticated client's additional contacts. The primary contact cannot be deleted
    (409). 404 existence-hiding for foreign/missing contacts.

    Args:
        contact_id (int):  Example: 88.
        confirm (bool | Unset):
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteContactResponse200 | Error
    """

    return (
        await asyncio_detailed(
            contact_id=contact_id,
            client=client,
            confirm=confirm,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
