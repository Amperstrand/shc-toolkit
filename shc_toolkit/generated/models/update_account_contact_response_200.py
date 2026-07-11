from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_contact_update_response import AccountContactUpdateResponse


T = TypeVar("T", bound="UpdateAccountContactResponse200")


@_attrs_define
class UpdateAccountContactResponse200:
    """
    Attributes:
        data (AccountContactUpdateResponse):  Example: {'contact_updated_at': '2026-05-05T23:15:42+00:00',
            'email_verification_required': True}.
    """

    data: AccountContactUpdateResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_contact_update_response import (
            AccountContactUpdateResponse,
        )

        d = dict(src_dict)
        data = AccountContactUpdateResponse.from_dict(d.pop("data"))

        update_account_contact_response_200 = cls(
            data=data,
        )

        update_account_contact_response_200.additional_properties = d
        return update_account_contact_response_200

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
