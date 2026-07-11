from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UpdateVmDataPreferencesResponse200DataNotify")


@_attrs_define
class UpdateVmDataPreferencesResponse200DataNotify:
    """
    Attributes:
        success (bool):
        failed (bool):
        limit (bool):
        auto_deleted (bool):
    """

    success: bool
    failed: bool
    limit: bool
    auto_deleted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        failed = self.failed

        limit = self.limit

        auto_deleted = self.auto_deleted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "failed": failed,
                "limit": limit,
                "auto_deleted": auto_deleted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success")

        failed = d.pop("failed")

        limit = d.pop("limit")

        auto_deleted = d.pop("auto_deleted")

        update_vm_data_preferences_response_200_data_notify = cls(
            success=success,
            failed=failed,
            limit=limit,
            auto_deleted=auto_deleted,
        )

        update_vm_data_preferences_response_200_data_notify.additional_properties = d
        return update_vm_data_preferences_response_200_data_notify

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
