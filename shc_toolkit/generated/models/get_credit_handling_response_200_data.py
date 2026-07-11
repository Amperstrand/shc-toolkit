from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.get_credit_handling_response_200_data_thresholds import (
        GetCreditHandlingResponse200DataThresholds,
    )


T = TypeVar("T", bound="GetCreditHandlingResponse200Data")


@_attrs_define
class GetCreditHandlingResponse200Data:
    """
    Attributes:
        credit_enabled (bool):  Example: True.
        thresholds (GetCreditHandlingResponse200DataThresholds): Map of ISO-4217 currency code to threshold string
            (4dp). Example: {'USD': '10.0000'}.
    """

    credit_enabled: bool
    thresholds: GetCreditHandlingResponse200DataThresholds

    def to_dict(self) -> dict[str, Any]:
        credit_enabled = self.credit_enabled

        thresholds = self.thresholds.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "credit_enabled": credit_enabled,
                "thresholds": thresholds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_credit_handling_response_200_data_thresholds import (
            GetCreditHandlingResponse200DataThresholds,
        )

        d = dict(src_dict)
        credit_enabled = d.pop("credit_enabled")

        thresholds = GetCreditHandlingResponse200DataThresholds.from_dict(
            d.pop("thresholds")
        )

        get_credit_handling_response_200_data = cls(
            credit_enabled=credit_enabled,
            thresholds=thresholds,
        )

        return get_credit_handling_response_200_data
