from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.enable_two_factor_response_200_data_mode import (
    EnableTwoFactorResponse200DataMode,
)

T = TypeVar("T", bound="EnableTwoFactorResponse200Data")


@_attrs_define
class EnableTwoFactorResponse200Data:
    """
    Attributes:
        enabled (bool):
        mode (EnableTwoFactorResponse200DataMode):
    """

    enabled: bool
    mode: EnableTwoFactorResponse200DataMode

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        mode = self.mode.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "enabled": enabled,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        mode = EnableTwoFactorResponse200DataMode(d.pop("mode"))

        enable_two_factor_response_200_data = cls(
            enabled=enabled,
            mode=mode,
        )

        return enable_two_factor_response_200_data
