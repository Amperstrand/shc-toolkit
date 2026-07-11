from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_api_keys_response_200_items_item_scope import (
    ListApiKeysResponse200ItemsItemScope,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListApiKeysResponse200ItemsItem")


@_attrs_define
class ListApiKeysResponse200ItemsItem:
    """
    Attributes:
        id (int | Unset):
        name (str | Unset):
        scope (ListApiKeysResponse200ItemsItemScope | Unset):
        key_prefix (str | Unset):
        created_at (str | Unset):
        expires_at (str | Unset):
        last_used_at (None | str | Unset):
        areas (list[str] | None | Unset): The key's native contact-permission area subset it is limited to, returned as
            an array of native area aliases (null for legacy rows). For keys minted since native area-scoping shipped this
            is an explicit array of aliases (an omitted 'areas' is materialized to the account's full permitted-area set,
            never stored unrestricted). A null value means a legacy key created before that change, which is treated as all
            areas (unrestricted).
    """

    id: int | Unset = UNSET
    name: str | Unset = UNSET
    scope: ListApiKeysResponse200ItemsItemScope | Unset = UNSET
    key_prefix: str | Unset = UNSET
    created_at: str | Unset = UNSET
    expires_at: str | Unset = UNSET
    last_used_at: None | str | Unset = UNSET
    areas: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        scope: str | Unset = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.value

        key_prefix = self.key_prefix

        created_at = self.created_at

        expires_at = self.expires_at

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        else:
            last_used_at = self.last_used_at

        areas: list[str] | None | Unset
        if isinstance(self.areas, Unset):
            areas = UNSET
        elif isinstance(self.areas, list):
            areas = self.areas

        else:
            areas = self.areas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if scope is not UNSET:
            field_dict["scope"] = scope
        if key_prefix is not UNSET:
            field_dict["key_prefix"] = key_prefix
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if areas is not UNSET:
            field_dict["areas"] = areas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _scope = d.pop("scope", UNSET)
        scope: ListApiKeysResponse200ItemsItemScope | Unset
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = ListApiKeysResponse200ItemsItemScope(_scope)

        key_prefix = d.pop("key_prefix", UNSET)

        created_at = d.pop("created_at", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        def _parse_last_used_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        def _parse_areas(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                areas_type_0 = cast(list[str], data)

                return areas_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        areas = _parse_areas(d.pop("areas", UNSET))

        list_api_keys_response_200_items_item = cls(
            id=id,
            name=name,
            scope=scope,
            key_prefix=key_prefix,
            created_at=created_at,
            expires_at=expires_at,
            last_used_at=last_used_at,
            areas=areas,
        )

        list_api_keys_response_200_items_item.additional_properties = d
        return list_api_keys_response_200_items_item

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
