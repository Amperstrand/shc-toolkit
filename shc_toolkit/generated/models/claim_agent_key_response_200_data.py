from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.claim_agent_key_response_200_data_scope import (
    ClaimAgentKeyResponse200DataScope,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ClaimAgentKeyResponse200Data")


@_attrs_define
class ClaimAgentKeyResponse200Data:
    """
    Attributes:
        key (str | Unset): The plaintext shc_live_ API key. Shown once.
        key_prefix (str | Unset):
        scope (ClaimAgentKeyResponse200DataScope | Unset):
        expires_at (datetime.datetime | None | Unset): The KEY's own expiry (the claim itself is now spent).
    """

    key: str | Unset = UNSET
    key_prefix: str | Unset = UNSET
    scope: ClaimAgentKeyResponse200DataScope | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        key_prefix = self.key_prefix

        scope: str | Unset = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.value

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if key_prefix is not UNSET:
            field_dict["key_prefix"] = key_prefix
        if scope is not UNSET:
            field_dict["scope"] = scope
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key", UNSET)

        key_prefix = d.pop("key_prefix", UNSET)

        _scope = d.pop("scope", UNSET)
        scope: ClaimAgentKeyResponse200DataScope | Unset
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = ClaimAgentKeyResponse200DataScope(_scope)

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        claim_agent_key_response_200_data = cls(
            key=key,
            key_prefix=key_prefix,
            scope=scope,
            expires_at=expires_at,
        )

        claim_agent_key_response_200_data.additional_properties = d
        return claim_agent_key_response_200_data

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
