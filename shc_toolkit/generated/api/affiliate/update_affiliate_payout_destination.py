from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.affiliate_payout_destination_update import (
    AffiliatePayoutDestinationUpdate,
)
from ...models.error import Error
from ...models.update_affiliate_payout_destination_response_200 import (
    UpdateAffiliatePayoutDestinationResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AffiliatePayoutDestinationUpdate,
    x_user_api_otp: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_user_api_otp, Unset):
        headers["X-User-Api-OTP"] = x_user_api_otp

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/affiliate/payout-destination",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UpdateAffiliatePayoutDestinationResponse200 | None:
    if response.status_code == 200:
        response_200 = UpdateAffiliatePayoutDestinationResponse200.from_dict(
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
) -> Response[Error | UpdateAffiliatePayoutDestinationResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AffiliatePayoutDestinationUpdate,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateAffiliatePayoutDestinationResponse200]:
    r"""Set the affiliate payout destination

     Sets, replaces, or clears the affiliate's Bitcoin payout destination(s). Send `payout_onchain` (an
    extended public key — xpub/ypub/zpub and testnet variants — or a single mainnet address) and/or
    `payout_lightning` (a Lightning Address, LNURL, or BOLT11 invoice). A field present with an empty
    string `\"\"` clears that destination; a field omitted is left unchanged. Validation matches the
    client portal exactly. Returns `404 not_found` if the client is not enrolled. Returns the resulting
    destination.

    Args:
        x_user_api_otp (str | Unset):
        body (AffiliatePayoutDestinationUpdate): At least one field required. Empty string clears
            that destination; omitted leaves it unchanged. Example: {'payout_onchain':
            'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateAffiliatePayoutDestinationResponse200]
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
    client: AuthenticatedClient | Client,
    body: AffiliatePayoutDestinationUpdate,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateAffiliatePayoutDestinationResponse200 | None:
    r"""Set the affiliate payout destination

     Sets, replaces, or clears the affiliate's Bitcoin payout destination(s). Send `payout_onchain` (an
    extended public key — xpub/ypub/zpub and testnet variants — or a single mainnet address) and/or
    `payout_lightning` (a Lightning Address, LNURL, or BOLT11 invoice). A field present with an empty
    string `\"\"` clears that destination; a field omitted is left unchanged. Validation matches the
    client portal exactly. Returns `404 not_found` if the client is not enrolled. Returns the resulting
    destination.

    Args:
        x_user_api_otp (str | Unset):
        body (AffiliatePayoutDestinationUpdate): At least one field required. Empty string clears
            that destination; omitted leaves it unchanged. Example: {'payout_onchain':
            'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateAffiliatePayoutDestinationResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        x_user_api_otp=x_user_api_otp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AffiliatePayoutDestinationUpdate,
    x_user_api_otp: str | Unset = UNSET,
) -> Response[Error | UpdateAffiliatePayoutDestinationResponse200]:
    r"""Set the affiliate payout destination

     Sets, replaces, or clears the affiliate's Bitcoin payout destination(s). Send `payout_onchain` (an
    extended public key — xpub/ypub/zpub and testnet variants — or a single mainnet address) and/or
    `payout_lightning` (a Lightning Address, LNURL, or BOLT11 invoice). A field present with an empty
    string `\"\"` clears that destination; a field omitted is left unchanged. Validation matches the
    client portal exactly. Returns `404 not_found` if the client is not enrolled. Returns the resulting
    destination.

    Args:
        x_user_api_otp (str | Unset):
        body (AffiliatePayoutDestinationUpdate): At least one field required. Empty string clears
            that destination; omitted leaves it unchanged. Example: {'payout_onchain':
            'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateAffiliatePayoutDestinationResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        x_user_api_otp=x_user_api_otp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: AffiliatePayoutDestinationUpdate,
    x_user_api_otp: str | Unset = UNSET,
) -> Error | UpdateAffiliatePayoutDestinationResponse200 | None:
    r"""Set the affiliate payout destination

     Sets, replaces, or clears the affiliate's Bitcoin payout destination(s). Send `payout_onchain` (an
    extended public key — xpub/ypub/zpub and testnet variants — or a single mainnet address) and/or
    `payout_lightning` (a Lightning Address, LNURL, or BOLT11 invoice). A field present with an empty
    string `\"\"` clears that destination; a field omitted is left unchanged. Validation matches the
    client portal exactly. Returns `404 not_found` if the client is not enrolled. Returns the resulting
    destination.

    Args:
        x_user_api_otp (str | Unset):
        body (AffiliatePayoutDestinationUpdate): At least one field required. Empty string clears
            that destination; omitted leaves it unchanged. Example: {'payout_onchain':
            'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateAffiliatePayoutDestinationResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_user_api_otp=x_user_api_otp,
        )
    ).parsed
