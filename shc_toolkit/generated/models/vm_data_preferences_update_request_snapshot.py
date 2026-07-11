from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmDataPreferencesUpdateRequestSnapshot")


@_attrs_define
class VmDataPreferencesUpdateRequestSnapshot:
    """Backup or snapshot scheduling preferences. Only the keys present are updated (PATCH semantics).

    Attributes:
        retention (str | Unset): A configured retention preset key, the literal `keep-all`, or a comma-separated
            `keep-<unit>=<n>` policy (units: last, hourly, daily, weekly, monthly, yearly). Example: keep-daily=7,keep-
            weekly=4.
        auto_days (list[str] | Unset): Days the automatic job runs (configured schedule-day keys). Example: ['mon',
            'thu'].
        auto_time (str | Unset): Hour the automatic job runs, in `HH:00` form. Example: 03:00.
    """

    retention: str | Unset = UNSET
    auto_days: list[str] | Unset = UNSET
    auto_time: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        retention = self.retention

        auto_days: list[str] | Unset = UNSET
        if not isinstance(self.auto_days, Unset):
            auto_days = self.auto_days

        auto_time = self.auto_time

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if retention is not UNSET:
            field_dict["retention"] = retention
        if auto_days is not UNSET:
            field_dict["auto_days"] = auto_days
        if auto_time is not UNSET:
            field_dict["auto_time"] = auto_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        retention = d.pop("retention", UNSET)

        auto_days = cast(list[str], d.pop("auto_days", UNSET))

        auto_time = d.pop("auto_time", UNSET)

        vm_data_preferences_update_request_snapshot = cls(
            retention=retention,
            auto_days=auto_days,
            auto_time=auto_time,
        )

        return vm_data_preferences_update_request_snapshot
