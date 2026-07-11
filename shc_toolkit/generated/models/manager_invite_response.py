from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.manager_invite_response_status import ManagerInviteResponseStatus

T = TypeVar("T", bound="ManagerInviteResponse")


@_attrs_define
class ManagerInviteResponse:
    """
    Attributes:
        invited (bool):  Example: True.
        email (str):
        status (ManagerInviteResponseStatus): 'pending' = invitation email sent to an existing same-company account;
            'invalid' = no matching account, recorded without an email (stock Blesta behavior). Example: pending.
        permissions (list[str]):
        created_at (datetime.datetime):
    """

    invited: bool
    email: str
    status: ManagerInviteResponseStatus
    permissions: list[str]
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        invited = self.invited

        email = self.email

        status = self.status.value

        permissions = self.permissions

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "invited": invited,
                "email": email,
                "status": status,
                "permissions": permissions,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        invited = d.pop("invited")

        email = d.pop("email")

        status = ManagerInviteResponseStatus(d.pop("status"))

        permissions = cast(list[str], d.pop("permissions"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        manager_invite_response = cls(
            invited=invited,
            email=email,
            status=status,
            permissions=permissions,
            created_at=created_at,
        )

        return manager_invite_response
