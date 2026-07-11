from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_api_key_body_areas_item import CreateApiKeyBodyAreasItem
from ..models.create_api_key_body_scope import CreateApiKeyBodyScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateApiKeyBody")


@_attrs_define
class CreateApiKeyBody:
    """
    Example:
        {'name': 'ci-integration', 'scope': 'operate', 'expires_in_days': 90}

    Attributes:
        name (str):
        scope (CreateApiKeyBodyScope | Unset): read=GET only; operate=ops but no money/billing/credentials; full=all
            except credential management
        expires_in_days (int | Unset):  Default: 90.
        areas (list[CreateApiKeyBodyAreasItem] | Unset): OPTIONAL. Native Blesta contact-permission area aliases this
            key may reach (ANDed with 'scope'). Omit to materialize the key to the account's FULL permitted-area set (the
            key is never stored area-unrestricted/null). Each value is validated against the account's native permission
            vocabulary; unknown areas are rejected 400, and a present-but-empty array is rejected 400 (omit the field
            instead). A key may only call operations whose x-required-area is in its set; identity/credential routes
            (x-required-area=__identity__) are never reachable by any key.
    """

    name: str
    scope: CreateApiKeyBodyScope | Unset = UNSET
    expires_in_days: int | Unset = 90
    areas: list[CreateApiKeyBodyAreasItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        scope: str | Unset = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.value

        expires_in_days = self.expires_in_days

        areas: list[str] | Unset = UNSET
        if not isinstance(self.areas, Unset):
            areas = []
            for areas_item_data in self.areas:
                areas_item = areas_item_data.value
                areas.append(areas_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if scope is not UNSET:
            field_dict["scope"] = scope
        if expires_in_days is not UNSET:
            field_dict["expires_in_days"] = expires_in_days
        if areas is not UNSET:
            field_dict["areas"] = areas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        _scope = d.pop("scope", UNSET)
        scope: CreateApiKeyBodyScope | Unset
        if isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = CreateApiKeyBodyScope(_scope)

        expires_in_days = d.pop("expires_in_days", UNSET)

        _areas = d.pop("areas", UNSET)
        areas: list[CreateApiKeyBodyAreasItem] | Unset = UNSET
        if _areas is not UNSET:
            areas = []
            for areas_item_data in _areas:
                areas_item = CreateApiKeyBodyAreasItem(areas_item_data)

                areas.append(areas_item)

        create_api_key_body = cls(
            name=name,
            scope=scope,
            expires_in_days=expires_in_days,
            areas=areas,
        )

        create_api_key_body.additional_properties = d
        return create_api_key_body

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
