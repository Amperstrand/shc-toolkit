from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateApiKeyResponse201Data")


@_attrs_define
class CreateApiKeyResponse201Data:
    """
    Attributes:
        id (int | Unset):
        name (str | Unset):
        scope (str | Unset):
        key (str | Unset): The secret API key — shown ONCE, never retrievable again.
        key_prefix (str | Unset):
        created_at (str | Unset):
        expires_at (str | Unset):
    """

    id: int | Unset = UNSET
    name: str | Unset = UNSET
    scope: str | Unset = UNSET
    key: str | Unset = UNSET
    key_prefix: str | Unset = UNSET
    created_at: str | Unset = UNSET
    expires_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        scope = self.scope

        key = self.key

        key_prefix = self.key_prefix

        created_at = self.created_at

        expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if scope is not UNSET:
            field_dict["scope"] = scope
        if key is not UNSET:
            field_dict["key"] = key
        if key_prefix is not UNSET:
            field_dict["key_prefix"] = key_prefix
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        scope = d.pop("scope", UNSET)

        key = d.pop("key", UNSET)

        key_prefix = d.pop("key_prefix", UNSET)

        created_at = d.pop("created_at", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        create_api_key_response_201_data = cls(
            id=id,
            name=name,
            scope=scope,
            key=key,
            key_prefix=key_prefix,
            created_at=created_at,
            expires_at=expires_at,
        )

        create_api_key_response_201_data.additional_properties = d
        return create_api_key_response_201_data

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
