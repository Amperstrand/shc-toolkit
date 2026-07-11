from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="VmRuntimeOverview")


@_attrs_define
class VmRuntimeOverview:
    """Live power-state snapshot (subset of the Proxmox status/current; host-identifying fields are omitted).

    Attributes:
        raw_status (str):  Example: running.
        state (str): raw_status, or 'locked' when a lock is held. Example: running.
        locked (bool):
        lock (None | str): Lock reason when locked (e.g. backup, migrate, snapshot).
        cpu_percent (int):  Example: 3.
        mem_percent (int):  Example: 42.
    """

    raw_status: str
    state: str
    locked: bool
    lock: None | str
    cpu_percent: int
    mem_percent: int

    def to_dict(self) -> dict[str, Any]:
        raw_status = self.raw_status

        state = self.state

        locked = self.locked

        lock: None | str
        lock = self.lock

        cpu_percent = self.cpu_percent

        mem_percent = self.mem_percent

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "raw_status": raw_status,
                "state": state,
                "locked": locked,
                "lock": lock,
                "cpu_percent": cpu_percent,
                "mem_percent": mem_percent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        raw_status = d.pop("raw_status")

        state = d.pop("state")

        locked = d.pop("locked")

        def _parse_lock(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        lock = _parse_lock(d.pop("lock"))

        cpu_percent = d.pop("cpu_percent")

        mem_percent = d.pop("mem_percent")

        vm_runtime_overview = cls(
            raw_status=raw_status,
            state=state,
            locked=locked,
            lock=lock,
            cpu_percent=cpu_percent,
            mem_percent=mem_percent,
        )

        return vm_runtime_overview
