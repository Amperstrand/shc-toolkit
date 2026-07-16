from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.vm_standby_response_ip_disposition import VmStandbyResponseIpDisposition
from ..models.vm_standby_response_lifecycle_state import VmStandbyResponseLifecycleState
from ..models.vm_standby_response_state import VmStandbyResponseState
from ..types import UNSET, Unset

T = TypeVar("T", bound="VmStandbyResponse")


@_attrs_define
class VmStandbyResponse:
    """
    Attributes:
        service_id (int):
        state (VmStandbyResponseState):
        lifecycle_state (VmStandbyResponseLifecycleState):
        standby_recurring (str):  Example: 6.8340.
        park_credit (str):  Example: 51.9194.
        ip_disposition (VmStandbyResponseIpDisposition):
        keep_ip (bool):
        op_id (None | str | Unset):
        job_id (int | None | Unset):
    """

    service_id: int
    state: VmStandbyResponseState
    lifecycle_state: VmStandbyResponseLifecycleState
    standby_recurring: str
    park_credit: str
    ip_disposition: VmStandbyResponseIpDisposition
    keep_ip: bool
    op_id: None | str | Unset = UNSET
    job_id: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        state = self.state.value

        lifecycle_state = self.lifecycle_state.value

        standby_recurring = self.standby_recurring

        park_credit = self.park_credit

        ip_disposition = self.ip_disposition.value

        keep_ip = self.keep_ip

        op_id: None | str | Unset
        if isinstance(self.op_id, Unset):
            op_id = UNSET
        else:
            op_id = self.op_id

        job_id: int | None | Unset
        if isinstance(self.job_id, Unset):
            job_id = UNSET
        else:
            job_id = self.job_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "state": state,
                "lifecycle_state": lifecycle_state,
                "standby_recurring": standby_recurring,
                "park_credit": park_credit,
                "ip_disposition": ip_disposition,
                "keep_ip": keep_ip,
            }
        )
        if op_id is not UNSET:
            field_dict["op_id"] = op_id
        if job_id is not UNSET:
            field_dict["job_id"] = job_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        state = VmStandbyResponseState(d.pop("state"))

        lifecycle_state = VmStandbyResponseLifecycleState(d.pop("lifecycle_state"))

        standby_recurring = d.pop("standby_recurring")

        park_credit = d.pop("park_credit")

        ip_disposition = VmStandbyResponseIpDisposition(d.pop("ip_disposition"))

        keep_ip = d.pop("keep_ip")

        def _parse_op_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        op_id = _parse_op_id(d.pop("op_id", UNSET))

        def _parse_job_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        job_id = _parse_job_id(d.pop("job_id", UNSET))

        vm_standby_response = cls(
            service_id=service_id,
            state=state,
            lifecycle_state=lifecycle_state,
            standby_recurring=standby_recurring,
            park_credit=park_credit,
            ip_disposition=ip_disposition,
            keep_ip=keep_ip,
            op_id=op_id,
            job_id=job_id,
        )

        return vm_standby_response
