from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UpdateAccountPreferencesResponse200DataEditable")


@_attrs_define
class UpdateAccountPreferencesResponse200DataEditable:
    """
    Example:
        {'autodebit': True, 'inv_address_to': True, 'tax_id': False, 'default_currency': False, 'inv_method': False,
            'language': False, 'receive_email_marketing': True}

    """

    additional_properties: dict[str, bool] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        update_account_preferences_response_200_data_editable = cls()

        update_account_preferences_response_200_data_editable.additional_properties = d
        return update_account_preferences_response_200_data_editable

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> bool:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: bool) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
