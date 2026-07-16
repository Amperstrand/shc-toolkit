from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_metric_series_values_item_item_type_2_type_4 import (
        VmMetricSeriesValuesItemItemType2Type4,
    )


T = TypeVar("T", bound="VmMetricSeries")


@_attrs_define
class VmMetricSeries:
    """One RRD metric series. values is an array of [epoch_seconds, value] pairs. divider (when present) converts raw
    values to display units.

        Attributes:
            name (str):  Example: CPU.
            values (list[list[bool | float | int | list[str] | None | str | VmMetricSeriesValuesItemItemType2Type4]]):
            divider (int | Unset): Divide raw values by this for display units (RAM 1073741824=GiB; disk/network
                1048576=MiB). Absent for CPU. Example: 1073741824.
    """

    name: str
    values: list[
        list[
            bool
            | float
            | int
            | list[str]
            | None
            | str
            | VmMetricSeriesValuesItemItemType2Type4
        ]
    ]
    divider: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.vm_metric_series_values_item_item_type_2_type_4 import (
            VmMetricSeriesValuesItemItemType2Type4,
        )

        name = self.name

        values = []
        for values_item_data in self.values:
            values_item = []
            for values_item_item_data in values_item_data:
                values_item_item: (
                    bool | dict[str, Any] | float | int | list[str] | None | str
                )
                if isinstance(
                    values_item_item_data, VmMetricSeriesValuesItemItemType2Type4
                ):
                    values_item_item = values_item_item_data.to_dict()
                elif isinstance(values_item_item_data, list):
                    values_item_item = values_item_item_data

                else:
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
        from ..models.vm_metric_series_values_item_item_type_2_type_4 import (
            VmMetricSeriesValuesItemItemType2Type4,
        )

        d = dict(src_dict)
        name = d.pop("name")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = []
            _values_item = values_item_data
            for values_item_item_data in _values_item:

                def _parse_values_item_item(
                    data: object,
                ) -> (
                    bool
                    | float
                    | int
                    | list[str]
                    | None
                    | str
                    | VmMetricSeriesValuesItemItemType2Type4
                ):
                    if data is None:
                        return data
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        values_item_item_type_2_type_4 = (
                            VmMetricSeriesValuesItemItemType2Type4.from_dict(data)
                        )

                        return values_item_item_type_2_type_4
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, list):
                            raise TypeError()
                        values_item_item_type_2_type_5 = cast(list[str], data)

                        return values_item_item_type_2_type_5
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    return cast(
                        bool
                        | float
                        | int
                        | list[str]
                        | None
                        | str
                        | VmMetricSeriesValuesItemItemType2Type4,
                        data,
                    )

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
