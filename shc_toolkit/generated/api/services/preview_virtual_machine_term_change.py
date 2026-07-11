from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.preview_virtual_machine_term_change_body import (
    PreviewVirtualMachineTermChangeBody,
)
from ...models.preview_virtual_machine_term_change_response_200 import (
    PreviewVirtualMachineTermChangeResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: int,
    *,
    body: PreviewVirtualMachineTermChangeBody,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vm/{service_id}/term/preview".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | PreviewVirtualMachineTermChangeResponse200 | None:
    if response.status_code == 200:
        response_200 = PreviewVirtualMachineTermChangeResponse200.from_dict(
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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | PreviewVirtualMachineTermChangeResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PreviewVirtualMachineTermChangeBody,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | PreviewVirtualMachineTermChangeResponse200]:
    """Preview the billing impact of a term change without committing it

     Preview the billing impact of a term change without committing it. Staged parity op: declared in the
    canonical 2.5 surface; handler lands separately (release_state=staged until then).

    Args:
        service_id (int):
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (PreviewVirtualMachineTermChangeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PreviewVirtualMachineTermChangeResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PreviewVirtualMachineTermChangeBody,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | PreviewVirtualMachineTermChangeResponse200 | None:
    """Preview the billing impact of a term change without committing it

     Preview the billing impact of a term change without committing it. Staged parity op: declared in the
    canonical 2.5 surface; handler lands separately (release_state=staged until then).

    Args:
        service_id (int):
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (PreviewVirtualMachineTermChangeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PreviewVirtualMachineTermChangeResponse200
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PreviewVirtualMachineTermChangeBody,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | PreviewVirtualMachineTermChangeResponse200]:
    """Preview the billing impact of a term change without committing it

     Preview the billing impact of a term change without committing it. Staged parity op: declared in the
    canonical 2.5 surface; handler lands separately (release_state=staged until then).

    Args:
        service_id (int):
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (PreviewVirtualMachineTermChangeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PreviewVirtualMachineTermChangeResponse200]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PreviewVirtualMachineTermChangeBody,
    idempotency_key: str | Unset = UNSET,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | PreviewVirtualMachineTermChangeResponse200 | None:
    """Preview the billing impact of a term change without committing it

     Preview the billing impact of a term change without committing it. Staged parity op: declared in the
    canonical 2.5 surface; handler lands separately (release_state=staged until then).

    Args:
        service_id (int):
        idempotency_key (str | Unset):
        x_user_api_otp (str | Unset):
        body (PreviewVirtualMachineTermChangeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PreviewVirtualMachineTermChangeResponse200
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            idempotency_key=idempotency_key,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
