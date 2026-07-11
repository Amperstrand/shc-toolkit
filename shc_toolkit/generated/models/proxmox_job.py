from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.proxmox_job_status import ProxmoxJobStatus
from ..models.proxmox_job_type import ProxmoxJobType

if TYPE_CHECKING:
    from ..models.proxmox_job_requested import ProxmoxJobRequested


T = TypeVar("T", bound="ProxmoxJob")


@_attrs_define
class ProxmoxJob:
    """Queued or historical background job for one owned VM service.

    Example:
        {'job_id': 912, 'service_id': 353, 'type': 'backup', 'status': 'running', 'progress': 45, 'step': 'Creating
            backup archive', 'error': None, 'requested': {'name': 'nightly-demo', 'mode': 'suspend', 'backup_id': None,
            'storage': 'pbs'}, 'created_at': '2026-04-17T01:23:45+00:00', 'completed_at': None}

    Attributes:
        job_id (int):  Example: 912.
        service_id (int):  Example: 353.
        type_ (ProxmoxJobType):  Example: backup.
        status (ProxmoxJobStatus):  Example: running.
        progress (int):  Example: 45.
        step (None | str): Current/last human-readable progress step. Sanitized at the API boundary so it never
            discloses the real Proxmox vmid, host node, or paths. Example: Creating backup archive.
        error (None | str):
        requested (ProxmoxJobRequested): Normalized request fields captured when the job was queued.
        created_at (datetime.datetime):  Example: 2026-04-17T01:23:45+00:00.
        completed_at (datetime.datetime | None):  Example: 2026-04-17T01:29:45+00:00.
    """

    job_id: int
    service_id: int
    type_: ProxmoxJobType
    status: ProxmoxJobStatus
    progress: int
    step: None | str
    error: None | str
    requested: ProxmoxJobRequested
    created_at: datetime.datetime
    completed_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        service_id = self.service_id

        type_ = self.type_.value

        status = self.status.value

        progress = self.progress

        step: None | str
        step = self.step

        error: None | str
        error = self.error

        requested = self.requested.to_dict()

        created_at = self.created_at.isoformat()

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "service_id": service_id,
                "type": type_,
                "status": status,
                "progress": progress,
                "step": step,
                "error": error,
                "requested": requested,
                "created_at": created_at,
                "completed_at": completed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.proxmox_job_requested import ProxmoxJobRequested

        d = dict(src_dict)
        job_id = d.pop("job_id")

        service_id = d.pop("service_id")

        type_ = ProxmoxJobType(d.pop("type"))

        status = ProxmoxJobStatus(d.pop("status"))

        progress = d.pop("progress")

        def _parse_step(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        step = _parse_step(d.pop("step"))

        def _parse_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error = _parse_error(d.pop("error"))

        requested = ProxmoxJobRequested.from_dict(d.pop("requested"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = datetime.datetime.fromisoformat(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        proxmox_job = cls(
            job_id=job_id,
            service_id=service_id,
            type_=type_,
            status=status,
            progress=progress,
            step=step,
            error=error,
            requested=requested,
            created_at=created_at,
            completed_at=completed_at,
        )

        proxmox_job.additional_properties = d
        return proxmox_job

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
