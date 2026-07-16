from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.batch_sub_request import BatchSubRequest
from ...models.problem import Problem
from ...models.submit_batch_response_200 import SubmitBatchResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: list[BatchSubRequest],
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    if not isinstance(x_user_api_confirm, Unset):
        headers["X-User-Api-Confirm"] = x_user_api_confirm

    if not isinstance(prefer, Unset):
        headers["Prefer"] = prefer

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/batch",
    }

    _kwargs["json"] = []
    for componentsschemas_batch_request_item_data in body:
        componentsschemas_batch_request_item = (
            componentsschemas_batch_request_item_data.to_dict()
        )
        _kwargs["json"].append(componentsschemas_batch_request_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Problem | SubmitBatchResponse200 | None:
    if response.status_code == 200:
        response_200 = SubmitBatchResponse200.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = Problem.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = Problem.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = Problem.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = Problem.from_dict(response.json())

        return response_429

    if response.status_code == 501:
        response_501 = Problem.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = Problem.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Problem | SubmitBatchResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: list[BatchSubRequest],
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
) -> Response[Problem | SubmitBatchResponse200]:
    """Submit batch sub-requests

     Submit an ordered array of live /user-api/v2 sub-requests. Responses are returned in the same order
    and echo each caller-supplied correlation id. Sub-requests are best-effort and independent: one
    failure is reported in that item and does not roll back successful siblings. Every sub-request is
    dispatched through the same native guard chain as a standalone call, including authenticated
    principal, bearer scope, per-operation confirmation, ownership, rate accounting, and per-operation
    idempotency. A batch consumes one rate unit per sub-request. The wrapper itself requires
    Idempotency-Key; replaying the same key and body returns the cached BatchResponse without re-
    executing sub-requests. If any sub-request targets a confirmation-gated operation, the batch wrapper
    must also include X-User-Api-Confirm as an explicit batch-level acknowledgement; per-sub-request
    confirm values are still required for guarded sub-requests.

    Args:
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        prefer (str | Unset):
        body (list[BatchSubRequest]): Ordered array of batch sub-requests. The native dispatcher
            preserves order and evaluates each sub-request independently through the same guard chain
            as a direct call. Example: [{'id': 'vm-read', 'method': 'GET', 'path': '/vm/353'}, {'id':
            'events', 'method': 'GET', 'path': '/events?limit=10'}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Problem | SubmitBatchResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
        prefer=prefer,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: list[BatchSubRequest],
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
) -> Problem | SubmitBatchResponse200 | None:
    """Submit batch sub-requests

     Submit an ordered array of live /user-api/v2 sub-requests. Responses are returned in the same order
    and echo each caller-supplied correlation id. Sub-requests are best-effort and independent: one
    failure is reported in that item and does not roll back successful siblings. Every sub-request is
    dispatched through the same native guard chain as a standalone call, including authenticated
    principal, bearer scope, per-operation confirmation, ownership, rate accounting, and per-operation
    idempotency. A batch consumes one rate unit per sub-request. The wrapper itself requires
    Idempotency-Key; replaying the same key and body returns the cached BatchResponse without re-
    executing sub-requests. If any sub-request targets a confirmation-gated operation, the batch wrapper
    must also include X-User-Api-Confirm as an explicit batch-level acknowledgement; per-sub-request
    confirm values are still required for guarded sub-requests.

    Args:
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        prefer (str | Unset):
        body (list[BatchSubRequest]): Ordered array of batch sub-requests. The native dispatcher
            preserves order and evaluates each sub-request independently through the same guard chain
            as a direct call. Example: [{'id': 'vm-read', 'method': 'GET', 'path': '/vm/353'}, {'id':
            'events', 'method': 'GET', 'path': '/events?limit=10'}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Problem | SubmitBatchResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
        prefer=prefer,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: list[BatchSubRequest],
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
) -> Response[Problem | SubmitBatchResponse200]:
    """Submit batch sub-requests

     Submit an ordered array of live /user-api/v2 sub-requests. Responses are returned in the same order
    and echo each caller-supplied correlation id. Sub-requests are best-effort and independent: one
    failure is reported in that item and does not roll back successful siblings. Every sub-request is
    dispatched through the same native guard chain as a standalone call, including authenticated
    principal, bearer scope, per-operation confirmation, ownership, rate accounting, and per-operation
    idempotency. A batch consumes one rate unit per sub-request. The wrapper itself requires
    Idempotency-Key; replaying the same key and body returns the cached BatchResponse without re-
    executing sub-requests. If any sub-request targets a confirmation-gated operation, the batch wrapper
    must also include X-User-Api-Confirm as an explicit batch-level acknowledgement; per-sub-request
    confirm values are still required for guarded sub-requests.

    Args:
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        prefer (str | Unset):
        body (list[BatchSubRequest]): Ordered array of batch sub-requests. The native dispatcher
            preserves order and evaluates each sub-request independently through the same guard chain
            as a direct call. Example: [{'id': 'vm-read', 'method': 'GET', 'path': '/vm/353'}, {'id':
            'events', 'method': 'GET', 'path': '/events?limit=10'}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Problem | SubmitBatchResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
        x_user_api_confirm=x_user_api_confirm,
        prefer=prefer,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: list[BatchSubRequest],
    idempotency_key: str,
    x_user_api_confirm: str | Unset = UNSET,
    prefer: str | Unset = UNSET,
) -> Problem | SubmitBatchResponse200 | None:
    """Submit batch sub-requests

     Submit an ordered array of live /user-api/v2 sub-requests. Responses are returned in the same order
    and echo each caller-supplied correlation id. Sub-requests are best-effort and independent: one
    failure is reported in that item and does not roll back successful siblings. Every sub-request is
    dispatched through the same native guard chain as a standalone call, including authenticated
    principal, bearer scope, per-operation confirmation, ownership, rate accounting, and per-operation
    idempotency. A batch consumes one rate unit per sub-request. The wrapper itself requires
    Idempotency-Key; replaying the same key and body returns the cached BatchResponse without re-
    executing sub-requests. If any sub-request targets a confirmation-gated operation, the batch wrapper
    must also include X-User-Api-Confirm as an explicit batch-level acknowledgement; per-sub-request
    confirm values are still required for guarded sub-requests.

    Args:
        idempotency_key (str):
        x_user_api_confirm (str | Unset):
        prefer (str | Unset):
        body (list[BatchSubRequest]): Ordered array of batch sub-requests. The native dispatcher
            preserves order and evaluates each sub-request independently through the same guard chain
            as a direct call. Example: [{'id': 'vm-read', 'method': 'GET', 'path': '/vm/353'}, {'id':
            'events', 'method': 'GET', 'path': '/events?limit=10'}].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Problem | SubmitBatchResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
            x_user_api_confirm=x_user_api_confirm,
            prefer=prefer,
        )
    ).parsed
