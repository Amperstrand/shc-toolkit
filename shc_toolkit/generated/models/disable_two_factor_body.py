from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DisableTwoFactorBody")


@_attrs_define
class DisableTwoFactorBody:
    """
    Attributes:
        current_password (str): The account's current login password.
    """

    current_password: str

    def to_dict(self) -> dict[str, Any]:
        current_password = self.current_password

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "current_password": current_password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        current_password = d.pop("current_password")

        disable_two_factor_body = cls(
            current_password=current_password,
        )

        return disable_two_factor_body
