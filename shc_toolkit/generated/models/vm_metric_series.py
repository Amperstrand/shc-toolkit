from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmMetricSeries")


@_attrs_define
class VmMetricSeries:
    """One RRD metric series. values is an array of [epoch_seconds, value] pairs. divider (when present) converts raw
    values to display units.

        Attributes:
            name (str):  Example: CPU.
            values (list[list[float | int]]):
            divider (int | Unset): Divide raw values by this for display units (RAM 1073741824=GiB; disk/network
                1048576=MiB). Absent for CPU. Example: 1073741824.
    """

    name: str
    values: list[list[float | int]]
    divider: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        values = []
        for values_item_data in self.values:
            values_item = []
            for values_item_item_data in values_item_data:
                values_item_item: float | int
                values_item_item = values_item_item_data
                values_item.append(values_item_item)

            values.append(values_item)

        divider = self.divider

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "values": values,
            }
        )
        if divider is not UNSET:
            field_dict["divider"] = divider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = []
            _values_item = values_item_data
            for values_item_item_data in _values_item:

                def _parse_values_item_item(data: object) -> float | int:
                    return cast(float | int, data)

                values_item_item = _parse_values_item_item(values_item_item_data)

                values_item.append(values_item_item)

            values.append(values_item)

        divider = d.pop("divider", UNSET)

        vm_metric_series = cls(
            name=name,
            values=values,
            divider=divider,
        )

        return vm_metric_series
