from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmDataPreferencesUpdateRequestNotify")


@_attrs_define
class VmDataPreferencesUpdateRequestNotify:
    """Notification toggles. Each accepts a JSON boolean or the strings on/off/true/false/1/0.

    Attributes:
        success (bool | Unset):  Example: True.
        failed (bool | Unset):  Example: True.
        limit (bool | Unset):
        auto_deleted (bool | Unset):
    """

    success: bool | Unset = UNSET
    failed: bool | Unset = UNSET
    limit: bool | Unset = UNSET
    auto_deleted: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        failed = self.failed

        limit = self.limit

        auto_deleted = self.auto_deleted

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if success is not UNSET:
            field_dict["success"] = success
        if failed is not UNSET:
            field_dict["failed"] = failed
        if limit is not UNSET:
            field_dict["limit"] = limit
        if auto_deleted is not UNSET:
            field_dict["auto_deleted"] = auto_deleted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        failed = d.pop("failed", UNSET)

        limit = d.pop("limit", UNSET)

        auto_deleted = d.pop("auto_deleted", UNSET)

        vm_data_preferences_update_request_notify = cls(
            success=success,
            failed=failed,
            limit=limit,
            auto_deleted=auto_deleted,
        )

        return vm_data_preferences_update_request_notify
