from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.register_api_key_scope import (
    RegisterApiKeyScope,
    check_register_api_key_scope,
)

T = TypeVar("T", bound="RegisterApiKey")


@_attrs_define
class RegisterApiKey:
    """A customer API key minted at registration. The plaintext `key` is shown ONCE."""

    key: str
    """ The secret API key (Bearer credential), shown once and never retrievable again. Begins with 'shc_live_'. """
    key_prefix: str
    """ Non-secret display prefix (first 12 characters of the key). """
    scope: RegisterApiKeyScope
    """ Key scope (the requested 'scope', defaulting to 'operate'). The /register endpoint mints only read or
    operate keys; no scope can reach identity/credential routes. """
    expires_at: str
    """ Key expiry timestamp (90 days after creation). """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        key_prefix = self.key_prefix

        scope: str = self.scope

        expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "key_prefix": key_prefix,
                "scope": scope,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        key = d.pop("key")

        key_prefix = d.pop("key_prefix")

        scope = check_register_api_key_scope(d.pop("scope"))

        expires_at = d.pop("expires_at")

        register_api_key = cls(
            key=key,
            key_prefix=key_prefix,
            scope=scope,
            expires_at=expires_at,
        )

        register_api_key.additional_properties = d
        return register_api_key

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
