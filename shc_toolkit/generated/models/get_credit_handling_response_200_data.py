from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.get_credit_handling_response_200_data_thresholds_type_0 import (
        GetCreditHandlingResponse200DataThresholdsType0,
    )


T = TypeVar("T", bound="GetCreditHandlingResponse200Data")


@_attrs_define
class GetCreditHandlingResponse200Data:
    """
    Attributes:
        credit_enabled (bool):  Example: True.
        thresholds (GetCreditHandlingResponse200DataThresholdsType0 | list[str]):
    """

    credit_enabled: bool
    thresholds: GetCreditHandlingResponse200DataThresholdsType0 | list[str]

    def to_dict(self) -> dict[str, Any]:
        from ..models.get_credit_handling_response_200_data_thresholds_type_0 import (
            GetCreditHandlingResponse200DataThresholdsType0,
        )

        credit_enabled = self.credit_enabled

        thresholds: dict[str, Any] | list[str]
        if isinstance(self.thresholds, GetCreditHandlingResponse200DataThresholdsType0):
            thresholds = self.thresholds.to_dict()
        else:
            thresholds = self.thresholds

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
        from ..models.get_credit_handling_response_200_data_thresholds_type_0 import (
            GetCreditHandlingResponse200DataThresholdsType0,
        )

        d = dict(src_dict)
        credit_enabled = d.pop("credit_enabled")

        def _parse_thresholds(
            data: object,
        ) -> GetCreditHandlingResponse200DataThresholdsType0 | list[str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                thresholds_type_0 = (
                    GetCreditHandlingResponse200DataThresholdsType0.from_dict(data)
                )

                return thresholds_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, list):
                raise TypeError()
            thresholds_type_1 = cast(list[str], data)

            return thresholds_type_1

        thresholds = _parse_thresholds(d.pop("thresholds"))

        get_credit_handling_response_200_data = cls(
            credit_enabled=credit_enabled,
            thresholds=thresholds,
        )

        return get_credit_handling_response_200_data
