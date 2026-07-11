from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="VmActivityItem")


@_attrs_define
class VmActivityItem:
    """One Proxmox task. Infrastructure identifiers (UPID/node/PID/PVE user) are stripped for tenant isolation.

    Attributes:
        type_ (None | str):  Example: qmstart.
        status (str): PVE task exit status ('OK' on success), or 'running' when not yet finished. Example: OK.
        starttime (datetime.datetime | None):  Example: 2026-06-03T19:00:00+00:00.
        starttime_epoch (int | None):  Example: 1780542000.
        endtime (datetime.datetime | None):  Example: 2026-06-03T19:00:02+00:00.
        endtime_epoch (int | None):  Example: 1780542002.
    """

    type_: None | str
    status: str
    starttime: datetime.datetime | None
    starttime_epoch: int | None
    endtime: datetime.datetime | None
    endtime_epoch: int | None

    def to_dict(self) -> dict[str, Any]:
        type_: None | str
        type_ = self.type_

        status = self.status

        starttime: None | str
        if isinstance(self.starttime, datetime.datetime):
            starttime = self.starttime.isoformat()
        else:
            starttime = self.starttime

        starttime_epoch: int | None
        starttime_epoch = self.starttime_epoch

        endtime: None | str
        if isinstance(self.endtime, datetime.datetime):
            endtime = self.endtime.isoformat()
        else:
            endtime = self.endtime

        endtime_epoch: int | None
        endtime_epoch = self.endtime_epoch

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "status": status,
                "starttime": starttime,
                "starttime_epoch": starttime_epoch,
                "endtime": endtime,
                "endtime_epoch": endtime_epoch,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_type_(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        type_ = _parse_type_(d.pop("type"))

        status = d.pop("status")

        def _parse_starttime(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                starttime_type_0 = datetime.datetime.fromisoformat(data)

                return starttime_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        starttime = _parse_starttime(d.pop("starttime"))

        def _parse_starttime_epoch(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        starttime_epoch = _parse_starttime_epoch(d.pop("starttime_epoch"))

        def _parse_endtime(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                endtime_type_0 = datetime.datetime.fromisoformat(data)

                return endtime_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        endtime = _parse_endtime(d.pop("endtime"))

        def _parse_endtime_epoch(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        endtime_epoch = _parse_endtime_epoch(d.pop("endtime_epoch"))

        vm_activity_item = cls(
            type_=type_,
            status=status,
            starttime=starttime,
            starttime_epoch=starttime_epoch,
            endtime=endtime,
            endtime_epoch=endtime_epoch,
        )

        return vm_activity_item
