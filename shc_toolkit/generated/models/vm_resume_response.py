from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.vm_resume_response_lifecycle_state import (
    VmResumeResponseLifecycleState,
    check_vm_resume_response_lifecycle_state,
)
from ..models.vm_resume_response_state import (
    VmResumeResponseState,
    check_vm_resume_response_state,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="VmResumeResponse")


@_attrs_define
class VmResumeResponse:
    service_id: int
    state: VmResumeResponseState
    lifecycle_state: VmResumeResponseLifecycleState
    resume_charge: str
    op_id: None | str | Unset = UNSET
    job_id: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        state: str = self.state

        lifecycle_state: str = self.lifecycle_state

        resume_charge = self.resume_charge

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
                "resume_charge": resume_charge,
            }
        )
        if op_id is not UNSET:
            field_dict["op_id"] = op_id
        if job_id is not UNSET:
            field_dict["job_id"] = job_id

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        state = check_vm_resume_response_state(d.pop("state"))

        lifecycle_state = check_vm_resume_response_lifecycle_state(
            d.pop("lifecycle_state")
        )

        resume_charge = d.pop("resume_charge")

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

        vm_resume_response = cls(
            service_id=service_id,
            state=state,
            lifecycle_state=lifecycle_state,
            resume_charge=resume_charge,
            op_id=op_id,
            job_id=job_id,
        )

        return vm_resume_response
