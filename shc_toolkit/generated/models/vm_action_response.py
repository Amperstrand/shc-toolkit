from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.runtime_status import RuntimeStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.next_verify import NextVerify


T = TypeVar("T", bound="VmActionResponse")


@_attrs_define
class VmActionResponse:
    """
    Attributes:
        id (int):  Example: 353.
        action (str):  Example: restart.
        runtime_status (RuntimeStatus): Live Proxmox VM runtime state. Example: running.
        confirmed (bool):  Example: True.
        message (str):  Example: VM restart command sent successfully.
        expected_runtime_status (RuntimeStatus | Unset): Live Proxmox VM runtime state. Example: running.
        next_ (NextVerify | Unset): Verify pointer for a fire-and-confirm action (power verbs).
    """

    id: int
    action: str
    runtime_status: RuntimeStatus
    confirmed: bool
    message: str
    expected_runtime_status: RuntimeStatus | Unset = UNSET
    next_: NextVerify | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        action = self.action

        runtime_status = self.runtime_status.value

        confirmed = self.confirmed

        message = self.message

        expected_runtime_status: str | Unset = UNSET
        if not isinstance(self.expected_runtime_status, Unset):
            expected_runtime_status = self.expected_runtime_status.value

        next_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "action": action,
                "runtime_status": runtime_status,
                "confirmed": confirmed,
                "message": message,
            }
        )
        if expected_runtime_status is not UNSET:
            field_dict["expected_runtime_status"] = expected_runtime_status
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.next_verify import NextVerify

        d = dict(src_dict)
        id = d.pop("id")

        action = d.pop("action")

        runtime_status = RuntimeStatus(d.pop("runtime_status"))

        confirmed = d.pop("confirmed")

        message = d.pop("message")

        _expected_runtime_status = d.pop("expected_runtime_status", UNSET)
        expected_runtime_status: RuntimeStatus | Unset
        if isinstance(_expected_runtime_status, Unset):
            expected_runtime_status = UNSET
        else:
            expected_runtime_status = RuntimeStatus(_expected_runtime_status)

        _next_ = d.pop("next", UNSET)
        next_: NextVerify | Unset
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = NextVerify.from_dict(_next_)

        vm_action_response = cls(
            id=id,
            action=action,
            runtime_status=runtime_status,
            confirmed=confirmed,
            message=message,
            expected_runtime_status=expected_runtime_status,
            next_=next_,
        )

        vm_action_response.additional_properties = d
        return vm_action_response

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
