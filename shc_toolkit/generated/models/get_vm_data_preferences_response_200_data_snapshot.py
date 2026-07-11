from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetVmDataPreferencesResponse200DataSnapshot")


@_attrs_define
class GetVmDataPreferencesResponse200DataSnapshot:
    """
    Attributes:
        retention (str):
        auto_days (list[str]):
        auto_time (None | str):
    """

    retention: str
    auto_days: list[str]
    auto_time: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        retention = self.retention

        auto_days = self.auto_days

        auto_time: None | str
        auto_time = self.auto_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "retention": retention,
                "auto_days": auto_days,
                "auto_time": auto_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        retention = d.pop("retention")

        auto_days = cast(list[str], d.pop("auto_days"))

        def _parse_auto_time(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        auto_time = _parse_auto_time(d.pop("auto_time"))

        get_vm_data_preferences_response_200_data_snapshot = cls(
            retention=retention,
            auto_days=auto_days,
            auto_time=auto_time,
        )

        get_vm_data_preferences_response_200_data_snapshot.additional_properties = d
        return get_vm_data_preferences_response_200_data_snapshot

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
