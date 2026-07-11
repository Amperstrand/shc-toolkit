from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.managed_account_invitation_request_action import (
    ManagedAccountInvitationRequestAction,
)

T = TypeVar("T", bound="ManagedAccountInvitationRequest")


@_attrs_define
class ManagedAccountInvitationRequest:
    """Accept or decline a management invitation addressed to the authenticated client.

    Example:
        {'action': 'accept'}

    Attributes:
        action (ManagedAccountInvitationRequestAction): Whether to accept or decline the invitation. Example: accept.
    """

    action: ManagedAccountInvitationRequestAction

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "action": action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = ManagedAccountInvitationRequestAction(d.pop("action"))

        managed_account_invitation_request = cls(
            action=action,
        )

        return managed_account_invitation_request
