from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.update_account_preferences_response_200_data import (
        UpdateAccountPreferencesResponse200Data,
    )


T = TypeVar("T", bound="UpdateAccountPreferencesResponse200")


@_attrs_define
class UpdateAccountPreferencesResponse200:
    """
    Attributes:
        data (UpdateAccountPreferencesResponse200Data):
    """

    data: UpdateAccountPreferencesResponse200Data

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_account_preferences_response_200_data import (
            UpdateAccountPreferencesResponse200Data,
        )

        d = dict(src_dict)
        data = UpdateAccountPreferencesResponse200Data.from_dict(d.pop("data"))

        update_account_preferences_response_200 = cls(
            data=data,
        )

        return update_account_preferences_response_200
