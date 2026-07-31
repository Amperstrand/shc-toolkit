from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.register_request_scope import (
    RegisterRequestScope,
    check_register_request_scope,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterRequest")


@_attrs_define
class RegisterRequest:
    email: str
    """ The account login identifier (used as the HTTP Basic username). Must be a valid email address. """
    password: str
    """ Account password. Minimum 8 characters; no other complexity rule is imposed. """
    first_name: str
    last_name: str
    tos_accepted: bool
    """ REQUIRED. Must be true: the caller affirms the end user accepted SHC's Terms of Service
    (https://blesta.sovereignhybridcompute.com/tos). A missing, null, or false value is rejected 400 tos_required.
    Mirrors the web registration form's terms gate. """
    country: str | Unset = "US"
    """ ISO 3166-1 alpha-2 country code (case-insensitive; stored uppercased). Optional; defaults to US. Validated
    against the supported country list. """
    recovery_email: str | Unset = UNSET
    """ Optional alternate email for password-reset delivery. """
    scope: RegisterRequestScope | Unset = "operate"
    """ Optional scope for the API key minted at registration. Defaults to 'operate' (read + provision, never
    spend). The anonymous /register endpoint is capped to {read, operate}; full keys are issued only via your
    account settings (authenticated POST /account/api-keys) after you sign in. Note that no scope can reach
    identity/credential routes (api-keys, password, 2FA, contact, primary-identity PATCH /account) — those are
    Basic+OTP-only for every key. """

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        password = self.password

        first_name = self.first_name

        last_name = self.last_name

        tos_accepted = self.tos_accepted

        country = self.country

        recovery_email = self.recovery_email

        scope: str | Unset = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "tos_accepted": tos_accepted,
            }
        )
        if country is not UNSET:
            field_dict["country"] = country
        if recovery_email is not UNSET:
            field_dict["recovery_email"] = recovery_email
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        email = d.pop("email")

        password = d.pop("password")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        tos_accepted = d.pop("tos_accepted")

        country = d.pop("country", UNSET)

        recovery_email = d.pop("recovery_email", UNSET)

        _scope = d.pop("scope", UNSET)
        scope: RegisterRequestScope | Unset
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = check_register_request_scope(_scope)

        register_request = cls(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            tos_accepted=tos_accepted,
            country=country,
            recovery_email=recovery_email,
            scope=scope,
        )

        return register_request
