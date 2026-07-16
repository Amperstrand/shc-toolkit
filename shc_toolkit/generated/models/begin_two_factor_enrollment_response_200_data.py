from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="BeginTwoFactorEnrollmentResponse200Data")


@_attrs_define
class BeginTwoFactorEnrollmentResponse200Data:
    """
    Attributes:
        two_factor_key (str): 40-char hex TOTP secret; submit back to POST /account/2fa to enable.
        secret_base32 (str): Base32 secret for manual authenticator entry.
        otpauth_uri (str): otpauth:// URI for QR provisioning.
    """

    two_factor_key: str
    secret_base32: str
    otpauth_uri: str

    def to_dict(self) -> dict[str, Any]:
        two_factor_key = self.two_factor_key

        secret_base32 = self.secret_base32

        otpauth_uri = self.otpauth_uri

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "two_factor_key": two_factor_key,
                "secret_base32": secret_base32,
                "otpauth_uri": otpauth_uri,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        two_factor_key = d.pop("two_factor_key")

        secret_base32 = d.pop("secret_base32")

        otpauth_uri = d.pop("otpauth_uri")

        begin_two_factor_enrollment_response_200_data = cls(
            two_factor_key=two_factor_key,
            secret_base32=secret_base32,
            otpauth_uri=otpauth_uri,
        )

        return begin_two_factor_enrollment_response_200_data
