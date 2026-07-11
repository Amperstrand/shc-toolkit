from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="AffiliatePayoutDestination")


@_attrs_define
class AffiliatePayoutDestination:
    """
    Attributes:
        payout_onchain (None | str): Bitcoin on-chain destination (xpub/ypub/zpub or address), or null.
        payout_lightning (None | str): Lightning destination (Lightning Address, LNURL, or BOLT11), or null.
    """

    payout_onchain: None | str
    payout_lightning: None | str

    def to_dict(self) -> dict[str, Any]:
        payout_onchain: None | str
        payout_onchain = self.payout_onchain

        payout_lightning: None | str
        payout_lightning = self.payout_lightning

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "payout_onchain": payout_onchain,
                "payout_lightning": payout_lightning,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_payout_onchain(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        payout_onchain = _parse_payout_onchain(d.pop("payout_onchain"))

        def _parse_payout_lightning(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        payout_lightning = _parse_payout_lightning(d.pop("payout_lightning"))

        affiliate_payout_destination = cls(
            payout_onchain=payout_onchain,
            payout_lightning=payout_lightning,
        )

        return affiliate_payout_destination
