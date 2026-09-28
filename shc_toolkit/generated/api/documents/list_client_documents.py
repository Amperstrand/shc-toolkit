from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_client_documents_order import ListClientDocumentsOrder
from ...models.list_client_documents_response_200 import ListClientDocumentsResponse200
from ...models.list_client_documents_sort import ListClientDocumentsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    sort: ListClientDocumentsSort | Unset = ListClientDocumentsSort.DATE_ADDED,
    order: ListClientDocumentsOrder | Unset = ListClientDocumentsOrder.DESC,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/documents",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | ListClientDocumentsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListClientDocumentsResponse200.from_dict(response.json())

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | ListClientDocumentsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    sort: ListClientDocumentsSort | Unset = ListClientDocumentsSort.DATE_ADDED,
    order: ListClientDocumentsOrder | Unset = ListClientDocumentsOrder.DESC,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListClientDocumentsResponse200]:
    """List documents visible to the authenticated account

     List documents visible to the authenticated client using the live /v2 sort and pagination query
    parameters.

    Args:
        sort (ListClientDocumentsSort | Unset):  Default: ListClientDocumentsSort.DATE_ADDED.
        order (ListClientDocumentsOrder | Unset):  Default: ListClientDocumentsOrder.DESC.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListClientDocumentsResponse200]
    """

    kwargs = _get_kwargs(
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    sort: ListClientDocumentsSort | Unset = ListClientDocumentsSort.DATE_ADDED,
    order: ListClientDocumentsOrder | Unset = ListClientDocumentsOrder.DESC,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListClientDocumentsResponse200 | None:
    """List documents visible to the authenticated account

     List documents visible to the authenticated client using the live /v2 sort and pagination query
    parameters.

    Args:
        sort (ListClientDocumentsSort | Unset):  Default: ListClientDocumentsSort.DATE_ADDED.
        order (ListClientDocumentsOrder | Unset):  Default: ListClientDocumentsOrder.DESC.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListClientDocumentsResponse200
    """

    return sync_detailed(
        client=client,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    sort: ListClientDocumentsSort | Unset = ListClientDocumentsSort.DATE_ADDED,
    order: ListClientDocumentsOrder | Unset = ListClientDocumentsOrder.DESC,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | ListClientDocumentsResponse200]:
    """List documents visible to the authenticated account

     List documents visible to the authenticated client using the live /v2 sort and pagination query
    parameters.

    Args:
        sort (ListClientDocumentsSort | Unset):  Default: ListClientDocumentsSort.DATE_ADDED.
        order (ListClientDocumentsOrder | Unset):  Default: ListClientDocumentsOrder.DESC.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ListClientDocumentsResponse200]
    """

    kwargs = _get_kwargs(
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    sort: ListClientDocumentsSort | Unset = ListClientDocumentsSort.DATE_ADDED,
    order: ListClientDocumentsOrder | Unset = ListClientDocumentsOrder.DESC,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | ListClientDocumentsResponse200 | None:
    """List documents visible to the authenticated account

     List documents visible to the authenticated client using the live /v2 sort and pagination query
    parameters.

    Args:
        sort (ListClientDocumentsSort | Unset):  Default: ListClientDocumentsSort.DATE_ADDED.
        order (ListClientDocumentsOrder | Unset):  Default: ListClientDocumentsOrder.DESC.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ListClientDocumentsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            sort=sort,
            order=order,
            limit=limit,
            offset=offset,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
