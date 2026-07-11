from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.register_api_key_scope import RegisterApiKeyScope

T = TypeVar("T", bound="RegisterApiKey")


@_attrs_define
class RegisterApiKey:
    """A customer API key minted at registration. The plaintext `key` is shown ONCE.

    Attributes:
        key (str): The secret API key (Bearer credential), shown once and never retrievable again. Begins with
            'shc_live_'. Example: shc_live_xceMPQ3n8kZr2t6Vd0wQpYH1aLb9cF4uG7sJ2mN5kP8.
        key_prefix (str): Non-secret display prefix (first 12 characters of the key). Example: shc_live_xc.
        scope (RegisterApiKeyScope): Key scope (the requested 'scope', defaulting to 'operate'). The /register endpoint
            mints only read or operate keys; no scope can reach identity/credential routes. Example: operate.
        expires_at (str): Key expiry timestamp (90 days after creation). Example: 2026-09-07T12:00:00+00:00.
    """

    key: str
    key_prefix: str
    scope: RegisterApiKeyScope
    expires_at: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        key_prefix = self.key_prefix

        scope = self.scope.value

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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        key_prefix = d.pop("key_prefix")

        scope = RegisterApiKeyScope(d.pop("scope"))

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
