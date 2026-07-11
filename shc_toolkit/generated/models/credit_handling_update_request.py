from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.credit_handling_update_request_thresholds import (
        CreditHandlingUpdateRequestThresholds,
    )


T = TypeVar("T", bound="CreditHandlingUpdateRequest")


@_attrs_define
class CreditHandlingUpdateRequest:
    """Full replacement of the per-currency low-credit notification threshold map. An empty `thresholds` object clears all
    thresholds.

        Example:
            {'thresholds': {'USD': '10.00'}}

        Attributes:
            thresholds (CreditHandlingUpdateRequestThresholds): Map of ISO-4217 currency code to threshold amount. Each
                currency must exist for the company. Example: {'USD': '10.00'}.
    """

    thresholds: CreditHandlingUpdateRequestThresholds

    def to_dict(self) -> dict[str, Any]:
        thresholds = self.thresholds.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "thresholds": thresholds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.credit_handling_update_request_thresholds import (
            CreditHandlingUpdateRequestThresholds,
        )

        d = dict(src_dict)
        thresholds = CreditHandlingUpdateRequestThresholds.from_dict(
            d.pop("thresholds")
        )

        credit_handling_update_request = cls(
            thresholds=thresholds,
        )

        return credit_handling_update_request
