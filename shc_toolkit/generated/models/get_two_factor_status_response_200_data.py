from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.get_two_factor_status_response_200_data_mode import (
    GetTwoFactorStatusResponse200DataMode,
    check_get_two_factor_status_response_200_data_mode,
)

T = TypeVar("T", bound="GetTwoFactorStatusResponse200Data")


@_attrs_define
class GetTwoFactorStatusResponse200Data:
    enabled: bool
    mode: GetTwoFactorStatusResponse200DataMode

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        mode: str = self.mode

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "enabled": enabled,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        mode = check_get_two_factor_status_response_200_data_mode(d.pop("mode"))

        get_two_factor_status_response_200_data = cls(
            enabled=enabled,
            mode=mode,
        )

        return get_two_factor_status_response_200_data
