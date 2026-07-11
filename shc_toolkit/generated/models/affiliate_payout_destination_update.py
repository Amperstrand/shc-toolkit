from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AffiliatePayoutDestinationUpdate")


@_attrs_define
class AffiliatePayoutDestinationUpdate:
    """At least one field required. Empty string clears that destination; omitted leaves it unchanged.

    Example:
        {'payout_onchain': 'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq'}

    Attributes:
        payout_onchain (str | Unset): Extended public key (xpub/ypub/zpub, testnet variants) or a single mainnet
            address; "" to clear. Example: bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq.
        payout_lightning (str | Unset): Lightning Address, LNURL, or BOLT11 invoice; "" to clear. Example:
            satoshi@sovereignhybridcompute.com.
    """

    payout_onchain: str | Unset = UNSET
    payout_lightning: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        payout_onchain = self.payout_onchain

        payout_lightning = self.payout_lightning

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if payout_onchain is not UNSET:
            field_dict["payout_onchain"] = payout_onchain
        if payout_lightning is not UNSET:
            field_dict["payout_lightning"] = payout_lightning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        payout_onchain = d.pop("payout_onchain", UNSET)

        payout_lightning = d.pop("payout_lightning", UNSET)

        affiliate_payout_destination_update = cls(
            payout_onchain=payout_onchain,
            payout_lightning=payout_lightning,
        )

        return affiliate_payout_destination_update
