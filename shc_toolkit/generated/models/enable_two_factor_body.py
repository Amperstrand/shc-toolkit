from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="EnableTwoFactorBody")


@_attrs_define
class EnableTwoFactorBody:
    """
    Attributes:
        current_password (str): The account's current login password.
        two_factor_key (str): The hex key from POST /account/2fa/enrollment.
        otp (str): A current code from the authenticator app.
    """

    current_password: str
    two_factor_key: str
    otp: str

    def to_dict(self) -> dict[str, Any]:
        current_password = self.current_password

        two_factor_key = self.two_factor_key

        otp = self.otp

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "current_password": current_password,
                "two_factor_key": two_factor_key,
                "otp": otp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        current_password = d.pop("current_password")

        two_factor_key = d.pop("two_factor_key")

        otp = d.pop("otp")

        enable_two_factor_body = cls(
            current_password=current_password,
            two_factor_key=two_factor_key,
            otp=otp,
        )

        return enable_two_factor_body
