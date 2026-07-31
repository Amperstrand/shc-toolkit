from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.disable_two_factor_response_200_data_mode import (
    DisableTwoFactorResponse200DataMode,
    check_disable_two_factor_response_200_data_mode,
)

T = TypeVar("T", bound="DisableTwoFactorResponse200Data")


@_attrs_define
class DisableTwoFactorResponse200Data:
    enabled: bool
    mode: DisableTwoFactorResponse200DataMode

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

        mode = check_disable_two_factor_response_200_data_mode(d.pop("mode"))

        disable_two_factor_response_200_data = cls(
            enabled=enabled,
            mode=mode,
        )

        return disable_two_factor_response_200_data
