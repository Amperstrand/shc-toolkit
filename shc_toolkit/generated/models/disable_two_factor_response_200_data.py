from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.disable_two_factor_response_200_data_mode import (
    DisableTwoFactorResponse200DataMode,
)

T = TypeVar("T", bound="DisableTwoFactorResponse200Data")


@_attrs_define
class DisableTwoFactorResponse200Data:
    """
    Attributes:
        enabled (bool):
        mode (DisableTwoFactorResponse200DataMode):
    """

    enabled: bool
    mode: DisableTwoFactorResponse200DataMode

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

        mode = DisableTwoFactorResponse200DataMode(d.pop("mode"))

        disable_two_factor_response_200_data = cls(
            enabled=enabled,
            mode=mode,
        )

        return disable_two_factor_response_200_data
