from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.next_poll import NextPoll


T = TypeVar("T", bound="VmReinstallResponse")


@_attrs_define
class VmReinstallResponse:
    """
    Attributes:
        id (int):  Example: 353.
        action (str):  Example: reinstall.
        job_id (int): Id of the queued reinstall job; poll GET /vm/{service_id}/jobs/{job_id} for progress. Example:
            912.
        template (str):  Example: debian13-cloud.
        gui_choice (str): Server-resolved desktop/GUI provisioning choice for the reinstall (`none` when not
            applicable). Not client-settable. Example: none.
        message (str):  Example: VM reinstall initiated. This may take several minutes..
        next_ (NextPoll | Unset): Poll pointer for an async (queued-job) producer.
    """

    id: int
    action: str
    job_id: int
    template: str
    gui_choice: str
    message: str
    next_: NextPoll | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        action = self.action

        job_id = self.job_id

        template = self.template

        gui_choice = self.gui_choice

        message = self.message

        next_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "action": action,
                "job_id": job_id,
                "template": template,
                "gui_choice": gui_choice,
                "message": message,
            }
        )
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.next_poll import NextPoll

        d = dict(src_dict)
        id = d.pop("id")

        action = d.pop("action")

        job_id = d.pop("job_id")

        template = d.pop("template")

        gui_choice = d.pop("gui_choice")

        message = d.pop("message")

        _next_ = d.pop("next", UNSET)
        next_: NextPoll | Unset
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = NextPoll.from_dict(_next_)

        vm_reinstall_response = cls(
            id=id,
            action=action,
            job_id=job_id,
            template=template,
            gui_choice=gui_choice,
            message=message,
            next_=next_,
        )

        vm_reinstall_response.additional_properties = d
        return vm_reinstall_response

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
