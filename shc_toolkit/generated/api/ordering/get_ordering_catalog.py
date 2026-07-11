from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.orderable_plan_list import OrderablePlanList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ordering/catalog",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | OrderablePlanList | None:
    if response.status_code == 200:
        response_200 = OrderablePlanList.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 405:
        response_405 = Error.from_dict(response.json())

        return response_405

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
) -> Response[Error | OrderablePlanList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | OrderablePlanList]:
    """List buyable VM plans for the authenticated customer

     Returns a canonical paginated list of storefront-backed orderable VM plans visible to the
    authenticated customer. Each item includes pricing, embedded image metadata, and available order
    paths. Orderable OS templates currently include debian13-cloud (default), debian12-cloud,
    ubuntu2404-cloud, ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud,
    alpine323-cloud, devuan5-cloud, openbsd79-cloud, and the dedicated windows2022-byol (Bring Your Own
    License) product. The Operating System is the `template` configurable option and the optional
    Desktop Environment is the `gui_choice` option (none [default], gnome, kde, xfce, cinnamon, mate) on
    AlmaLinux 9; both appear under `config_options` in each plan with their full allowed value sets.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | OrderablePlanList]
    """

    kwargs = _get_kwargs(
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
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | OrderablePlanList | None:
    """List buyable VM plans for the authenticated customer

     Returns a canonical paginated list of storefront-backed orderable VM plans visible to the
    authenticated customer. Each item includes pricing, embedded image metadata, and available order
    paths. Orderable OS templates currently include debian13-cloud (default), debian12-cloud,
    ubuntu2404-cloud, ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud,
    alpine323-cloud, devuan5-cloud, openbsd79-cloud, and the dedicated windows2022-byol (Bring Your Own
    License) product. The Operating System is the `template` configurable option and the optional
    Desktop Environment is the `gui_choice` option (none [default], gnome, kde, xfce, cinnamon, mate) on
    AlmaLinux 9; both appear under `config_options` in each plan with their full allowed value sets.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | OrderablePlanList
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | OrderablePlanList]:
    """List buyable VM plans for the authenticated customer

     Returns a canonical paginated list of storefront-backed orderable VM plans visible to the
    authenticated customer. Each item includes pricing, embedded image metadata, and available order
    paths. Orderable OS templates currently include debian13-cloud (default), debian12-cloud,
    ubuntu2404-cloud, ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud,
    alpine323-cloud, devuan5-cloud, openbsd79-cloud, and the dedicated windows2022-byol (Bring Your Own
    License) product. The Operating System is the `template` configurable option and the optional
    Desktop Environment is the `gui_choice` option (none [default], gnome, kde, xfce, cinnamon, mate) on
    AlmaLinux 9; both appear under `config_options` in each plan with their full allowed value sets.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | OrderablePlanList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | OrderablePlanList | None:
    """List buyable VM plans for the authenticated customer

     Returns a canonical paginated list of storefront-backed orderable VM plans visible to the
    authenticated customer. Each item includes pricing, embedded image metadata, and available order
    paths. Orderable OS templates currently include debian13-cloud (default), debian12-cloud,
    ubuntu2404-cloud, ubuntu2204-cloud, fedora43-cloud, arch-cloud, nixos-cloud, almalinux9-cloud,
    alpine323-cloud, devuan5-cloud, openbsd79-cloud, and the dedicated windows2022-byol (Bring Your Own
    License) product. The Operating System is the `template` configurable option and the optional
    Desktop Environment is the `gui_choice` option (none [default], gnome, kde, xfce, cinnamon, mate) on
    AlmaLinux 9; both appear under `config_options` in each plan with their full allowed value sets.

    Args:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_user_api_otp (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | OrderablePlanList
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
