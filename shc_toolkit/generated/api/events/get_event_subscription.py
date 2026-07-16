from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_event_subscription_response_200 import (
    GetEventSubscriptionResponse200,
)
from ...models.problem import Problem
from ...types import Response


def _get_kwargs(
    event_subscription_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/event-subscriptions/{event_subscription_id}".format(
            event_subscription_id=quote(str(event_subscription_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetEventSubscriptionResponse200 | Problem | None:
    if response.status_code == 200:
        response_200 = GetEventSubscriptionResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Problem.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Problem.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Problem.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Problem.from_dict(response.json())

        return response_404

    if response.status_code == 405:
        response_405 = Problem.from_dict(response.json())

        return response_405

    if response.status_code == 413:
        response_413 = Problem.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Problem.from_dict(response.json())

        return response_415

    if response.status_code == 422:
        response_422 = Problem.from_dict(response.json())

        return response_422

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
) -> Response[GetEventSubscriptionResponse200 | Problem]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_subscription_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetEventSubscriptionResponse200 | Problem]:
    """Get event webhook subscription

     Reads one webhook subscription owned by the authenticated customer. Secrets are never returned;
    another customer's subscription id returns 404.

    Args:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetEventSubscriptionResponse200 | Problem]
    """

    kwargs = _get_kwargs(
        event_subscription_id=event_subscription_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_subscription_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetEventSubscriptionResponse200 | Problem | None:
    """Get event webhook subscription

     Reads one webhook subscription owned by the authenticated customer. Secrets are never returned;
    another customer's subscription id returns 404.

    Args:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetEventSubscriptionResponse200 | Problem
    """

    return sync_detailed(
        event_subscription_id=event_subscription_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    event_subscription_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetEventSubscriptionResponse200 | Problem]:
    """Get event webhook subscription

     Reads one webhook subscription owned by the authenticated customer. Secrets are never returned;
    another customer's subscription id returns 404.

    Args:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetEventSubscriptionResponse200 | Problem]
    """

    kwargs = _get_kwargs(
        event_subscription_id=event_subscription_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_subscription_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetEventSubscriptionResponse200 | Problem | None:
    """Get event webhook subscription

     Reads one webhook subscription owned by the authenticated customer. Secrets are never returned;
    another customer's subscription id returns 404.

    Args:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetEventSubscriptionResponse200 | Problem
    """

    return (
        await asyncio_detailed(
            event_subscription_id=event_subscription_id,
            client=client,
        )
    ).parsed
