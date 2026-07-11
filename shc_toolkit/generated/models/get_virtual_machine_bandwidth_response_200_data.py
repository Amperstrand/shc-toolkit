from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.get_virtual_machine_bandwidth_response_200_data_count_direction import (
    GetVirtualMachineBandwidthResponse200DataCountDirection,
)

T = TypeVar("T", bound="GetVirtualMachineBandwidthResponse200Data")


@_attrs_define
class GetVirtualMachineBandwidthResponse200Data:
    """
    Attributes:
        service_id (int):  Example: 451.
        used_bytes (int):  Example: 15010866192.
        used_gb (float):  Example: 13.98.
        limit_gb (int):  Example: 1000.
        count_direction (GetVirtualMachineBandwidthResponse200DataCountDirection):  Example: both.
        as_of (datetime.datetime | None):  Example: 2026-06-03T20:22:00+00:00.
        as_of_epoch (int | None): Unix seconds companion to as_of. Example: 1780544520.
    """

    service_id: int
    used_bytes: int
    used_gb: float
    limit_gb: int
    count_direction: GetVirtualMachineBandwidthResponse200DataCountDirection
    as_of: datetime.datetime | None
    as_of_epoch: int | None

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        used_bytes = self.used_bytes

        used_gb = self.used_gb

        limit_gb = self.limit_gb

        count_direction = self.count_direction.value

        as_of: None | str
        if isinstance(self.as_of, datetime.datetime):
            as_of = self.as_of.isoformat()
        else:
            as_of = self.as_of

        as_of_epoch: int | None
        as_of_epoch = self.as_of_epoch

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "used_bytes": used_bytes,
                "used_gb": used_gb,
                "limit_gb": limit_gb,
                "count_direction": count_direction,
                "as_of": as_of,
                "as_of_epoch": as_of_epoch,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        used_bytes = d.pop("used_bytes")

        used_gb = d.pop("used_gb")

        limit_gb = d.pop("limit_gb")

        count_direction = GetVirtualMachineBandwidthResponse200DataCountDirection(
            d.pop("count_direction")
        )

        def _parse_as_of(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                as_of_type_0 = datetime.datetime.fromisoformat(data)

                return as_of_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        as_of = _parse_as_of(d.pop("as_of"))

        def _parse_as_of_epoch(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        as_of_epoch = _parse_as_of_epoch(d.pop("as_of_epoch"))

        get_virtual_machine_bandwidth_response_200_data = cls(
            service_id=service_id,
            used_bytes=used_bytes,
            used_gb=used_gb,
            limit_gb=limit_gb,
            count_direction=count_direction,
            as_of=as_of,
            as_of_epoch=as_of_epoch,
        )

        return get_virtual_machine_bandwidth_response_200_data
