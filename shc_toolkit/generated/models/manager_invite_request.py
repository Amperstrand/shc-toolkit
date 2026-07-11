from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ManagerInviteRequest")


@_attrs_define
class ManagerInviteRequest:
    """Fields for inviting an account manager. Mirrors the portal add-manager form.

    Example:
        {'email': 'manager@example.com', 'permissions': ['client_invoices', 'client_services']}

    Attributes:
        email (str):  Example: manager@example.com.
        permissions (list[str]): Permission area keys to grant the manager (non-empty). Unknown keys are ignored; see
            GET /managers/permission-options. Example: ['client_invoices', 'client_services'].
    """

    email: str
    permissions: list[str]

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        permissions = self.permissions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "email": email,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        permissions = cast(list[str], d.pop("permissions"))

        manager_invite_request = cls(
            email=email,
            permissions=permissions,
        )

        return manager_invite_request
