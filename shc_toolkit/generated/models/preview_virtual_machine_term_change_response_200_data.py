from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.preview_virtual_machine_term_change_response_200_data_current import (
        PreviewVirtualMachineTermChangeResponse200DataCurrent,
    )
    from ..models.preview_virtual_machine_term_change_response_200_data_target import (
        PreviewVirtualMachineTermChangeResponse200DataTarget,
    )


T = TypeVar("T", bound="PreviewVirtualMachineTermChangeResponse200Data")


@_attrs_define
class PreviewVirtualMachineTermChangeResponse200Data:
    """
    Attributes:
        service_id (int):
        current (PreviewVirtualMachineTermChangeResponse200DataCurrent):
        target (PreviewVirtualMachineTermChangeResponse200DataTarget):
        due_on_change (str): Amount due to change term, as a fixed two-decimal money string.
        term_change_allowed (bool): Whether this client is allowed to change service term.
    """

    service_id: int
    current: PreviewVirtualMachineTermChangeResponse200DataCurrent
    target: PreviewVirtualMachineTermChangeResponse200DataTarget
    due_on_change: str
    term_change_allowed: bool

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        current = self.current.to_dict()

        target = self.target.to_dict()

        due_on_change = self.due_on_change

        term_change_allowed = self.term_change_allowed

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "service_id": service_id,
                "current": current,
                "target": target,
                "due_on_change": due_on_change,
                "term_change_allowed": term_change_allowed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.preview_virtual_machine_term_change_response_200_data_current import (
            PreviewVirtualMachineTermChangeResponse200DataCurrent,
        )
        from ..models.preview_virtual_machine_term_change_response_200_data_target import (
            PreviewVirtualMachineTermChangeResponse200DataTarget,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        current = PreviewVirtualMachineTermChangeResponse200DataCurrent.from_dict(
            d.pop("current")
        )

        target = PreviewVirtualMachineTermChangeResponse200DataTarget.from_dict(
            d.pop("target")
        )

        due_on_change = d.pop("due_on_change")

        term_change_allowed = d.pop("term_change_allowed")

        preview_virtual_machine_term_change_response_200_data = cls(
            service_id=service_id,
            current=current,
            target=target,
            due_on_change=due_on_change,
            term_change_allowed=term_change_allowed,
        )

        return preview_virtual_machine_term_change_response_200_data
