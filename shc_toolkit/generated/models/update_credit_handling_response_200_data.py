from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.update_credit_handling_response_200_data_thresholds import (
        UpdateCreditHandlingResponse200DataThresholds,
    )


T = TypeVar("T", bound="UpdateCreditHandlingResponse200Data")


@_attrs_define
class UpdateCreditHandlingResponse200Data:
    """
    Attributes:
        credit_enabled (bool):  Example: True.
        thresholds (UpdateCreditHandlingResponse200DataThresholds): Map of ISO-4217 currency code to threshold string
            (4dp). Example: {'USD': '10.0000'}.
    """

    credit_enabled: bool
    thresholds: UpdateCreditHandlingResponse200DataThresholds

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
        from ..models.update_credit_handling_response_200_data_thresholds import (
            UpdateCreditHandlingResponse200DataThresholds,
        )

        d = dict(src_dict)
        credit_enabled = d.pop("credit_enabled")

        thresholds = UpdateCreditHandlingResponse200DataThresholds.from_dict(
            d.pop("thresholds")
        )

        update_credit_handling_response_200_data = cls(
            credit_enabled=credit_enabled,
            thresholds=thresholds,
        )

        return update_credit_handling_response_200_data
