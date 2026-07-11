from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.managed_account_invitation_response_action import (
    ManagedAccountInvitationResponseAction,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ManagedAccountInvitationResponse")


@_attrs_define
class ManagedAccountInvitationResponse:
    """Result of accepting/declining a management invitation.

    Attributes:
        action (ManagedAccountInvitationResponseAction):  Example: accepted.
        managed_client_id (int): The client id this client now manages (on accept) or that the invitation referenced.
            Example: 4096.
        already_resolved (bool | Unset): Present and true when accept is a no-op because the invitation was already
            accepted (idempotent). Example: True.
    """

    action: ManagedAccountInvitationResponseAction
    managed_client_id: int
    already_resolved: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        managed_client_id = self.managed_client_id

        already_resolved = self.already_resolved

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "managed_client_id": managed_client_id,
            }
        )
        if already_resolved is not UNSET:
            field_dict["already_resolved"] = already_resolved

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = ManagedAccountInvitationResponseAction(d.pop("action"))

        managed_client_id = d.pop("managed_client_id")

        already_resolved = d.pop("already_resolved", UNSET)

        managed_account_invitation_response = cls(
            action=action,
            managed_client_id=managed_client_id,
            already_resolved=already_resolved,
        )

        managed_account_invitation_response.additional_properties = d
        return managed_account_invitation_response

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
