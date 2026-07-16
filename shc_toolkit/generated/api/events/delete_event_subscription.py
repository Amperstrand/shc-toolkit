from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_event_subscription_body import DeleteEventSubscriptionBody
from ...models.delete_event_subscription_response_200 import (
    DeleteEventSubscriptionResponse200,
)
from ...models.problem import Problem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    event_subscription_id: str,
    *,
    body: DeleteEventSubscriptionBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/event-subscriptions/{event_subscription_id}".format(
            event_subscription_id=quote(str(event_subscription_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeleteEventSubscriptionResponse200 | Problem | None:
    if response.status_code == 200:
        response_200 = DeleteEventSubscriptionResponse200.from_dict(response.json())

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
) -> Response[DeleteEventSubscriptionResponse200 | Problem]:
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
    body: DeleteEventSubscriptionBody | Unset = UNSET,
) -> Response[DeleteEventSubscriptionResponse200 | Problem]:
    """Delete event webhook subscription

     Deletes one webhook subscription owned by the authenticated customer and stops future delivery
    attempts. Existing queue and dead-letter artifacts for that subscription are removed during
    deletion.

    Args:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.
        body (DeleteEventSubscriptionBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteEventSubscriptionResponse200 | Problem]
    """

    kwargs = _get_kwargs(
        event_subscription_id=event_subscription_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_subscription_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteEventSubscriptionBody | Unset = UNSET,
) -> DeleteEventSubscriptionResponse200 | Problem | None:
    """Delete event webhook subscription

     Deletes one webhook subscription owned by the authenticated customer and stops future delivery
    attempts. Existing queue and dead-letter artifacts for that subscription are removed during
    deletion.

    Args:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.
        body (DeleteEventSubscriptionBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteEventSubscriptionResponse200 | Problem
    """

    return sync_detailed(
        event_subscription_id=event_subscription_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    event_subscription_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteEventSubscriptionBody | Unset = UNSET,
) -> Response[DeleteEventSubscriptionResponse200 | Problem]:
    """Delete event webhook subscription

     Deletes one webhook subscription owned by the authenticated customer and stops future delivery
    attempts. Existing queue and dead-letter artifacts for that subscription are removed during
    deletion.

    Args:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.
        body (DeleteEventSubscriptionBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteEventSubscriptionResponse200 | Problem]
    """

    kwargs = _get_kwargs(
        event_subscription_id=event_subscription_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_subscription_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeleteEventSubscriptionBody | Unset = UNSET,
) -> DeleteEventSubscriptionResponse200 | Problem | None:
    """Delete event webhook subscription

     Deletes one webhook subscription owned by the authenticated customer and stops future delivery
    attempts. Existing queue and dead-letter artifacts for that subscription are removed during
    deletion.

    Args:
        event_subscription_id (str):  Example: evsub_0123456789abcdef0123456789abcdef.
        body (DeleteEventSubscriptionBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteEventSubscriptionResponse200 | Problem
    """

    return (
        await asyncio_detailed(
            event_subscription_id=event_subscription_id,
            client=client,
            body=body,
        )
    ).parsed
