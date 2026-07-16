from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_events_response_200 import ListEventsResponse200
from ...models.problem import Problem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    virtual_machine_id: int | Unset = UNSET,
    fields: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
    if_none_match: str | Unset = UNSET,
    accept_encoding: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(prefer, Unset):
        headers["Prefer"] = prefer

    if not isinstance(if_none_match, Unset):
        headers["If-None-Match"] = if_none_match

    if not isinstance(accept_encoding, Unset):
        headers["Accept-Encoding"] = accept_encoding

    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    params["virtualMachineId"] = virtual_machine_id

    params["fields"] = fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/events",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ListEventsResponse200 | Problem | None:
    if response.status_code == 200:
        response_200 = ListEventsResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 304:
        response_304 = cast(Any, None)
        return response_304

    if response.status_code == 400:
        response_400 = Problem.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Problem.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Problem.from_dict(response.json())

        return response_403

    if response.status_code == 429:
        response_429 = Problem.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = Problem.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ListEventsResponse200 | Problem]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    virtual_machine_id: int | Unset = UNSET,
    fields: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
    if_none_match: str | Unset = UNSET,
    accept_encoding: str | Unset = UNSET,
) -> Response[Any | ListEventsResponse200 | Problem]:
    """List customer events

     poll-first customer domain event feed. Source precedence is: Blesta Services model/service logs
    first; billing/order state transitions second; redacted module/gateway events third. API request
    audit is a separate stream and actor=self_api_request is excluded by default. Webhook push
    registration, signing, retries, and delivery are intentionally not modeled in this build.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.
        virtual_machine_id (int | Unset):
        fields (str | Unset):
        prefer (str | Unset):
        if_none_match (str | Unset):
        accept_encoding (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ListEventsResponse200 | Problem]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        virtual_machine_id=virtual_machine_id,
        fields=fields,
        prefer=prefer,
        if_none_match=if_none_match,
        accept_encoding=accept_encoding,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    virtual_machine_id: int | Unset = UNSET,
    fields: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
    if_none_match: str | Unset = UNSET,
    accept_encoding: str | Unset = UNSET,
) -> Any | ListEventsResponse200 | Problem | None:
    """List customer events

     poll-first customer domain event feed. Source precedence is: Blesta Services model/service logs
    first; billing/order state transitions second; redacted module/gateway events third. API request
    audit is a separate stream and actor=self_api_request is excluded by default. Webhook push
    registration, signing, retries, and delivery are intentionally not modeled in this build.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.
        virtual_machine_id (int | Unset):
        fields (str | Unset):
        prefer (str | Unset):
        if_none_match (str | Unset):
        accept_encoding (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ListEventsResponse200 | Problem
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        virtual_machine_id=virtual_machine_id,
        fields=fields,
        prefer=prefer,
        if_none_match=if_none_match,
        accept_encoding=accept_encoding,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    virtual_machine_id: int | Unset = UNSET,
    fields: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
    if_none_match: str | Unset = UNSET,
    accept_encoding: str | Unset = UNSET,
) -> Response[Any | ListEventsResponse200 | Problem]:
    """List customer events

     poll-first customer domain event feed. Source precedence is: Blesta Services model/service logs
    first; billing/order state transitions second; redacted module/gateway events third. API request
    audit is a separate stream and actor=self_api_request is excluded by default. Webhook push
    registration, signing, retries, and delivery are intentionally not modeled in this build.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.
        virtual_machine_id (int | Unset):
        fields (str | Unset):
        prefer (str | Unset):
        if_none_match (str | Unset):
        accept_encoding (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ListEventsResponse200 | Problem]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        virtual_machine_id=virtual_machine_id,
        fields=fields,
        prefer=prefer,
        if_none_match=if_none_match,
        accept_encoding=accept_encoding,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    virtual_machine_id: int | Unset = UNSET,
    fields: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
    if_none_match: str | Unset = UNSET,
    accept_encoding: str | Unset = UNSET,
) -> Any | ListEventsResponse200 | Problem | None:
    """List customer events

     poll-first customer domain event feed. Source precedence is: Blesta Services model/service logs
    first; billing/order state transitions second; redacted module/gateway events third. API request
    audit is a separate stream and actor=self_api_request is excluded by default. Webhook push
    registration, signing, retries, and delivery are intentionally not modeled in this build.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.
        virtual_machine_id (int | Unset):
        fields (str | Unset):
        prefer (str | Unset):
        if_none_match (str | Unset):
        accept_encoding (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ListEventsResponse200 | Problem
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            virtual_machine_id=virtual_machine_id,
            fields=fields,
            prefer=prefer,
            if_none_match=if_none_match,
            accept_encoding=accept_encoding,
        )
    ).parsed
