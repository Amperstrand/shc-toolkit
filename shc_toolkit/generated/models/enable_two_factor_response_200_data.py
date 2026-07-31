from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.enable_two_factor_response_200_data_mode import (
    EnableTwoFactorResponse200DataMode,
    check_enable_two_factor_response_200_data_mode,
)

T = TypeVar("T", bound="EnableTwoFactorResponse200Data")


@_attrs_define
class EnableTwoFactorResponse200Data:
    enabled: bool
    mode: EnableTwoFactorResponse200DataMode

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

        mode = check_enable_two_factor_response_200_data_mode(d.pop("mode"))

        enable_two_factor_response_200_data = cls(
            enabled=enabled,
            mode=mode,
        )

        return enable_two_factor_response_200_data
