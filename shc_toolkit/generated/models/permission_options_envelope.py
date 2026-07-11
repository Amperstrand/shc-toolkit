from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.permission_options_envelope_permissions_item import (
        PermissionOptionsEnvelopePermissionsItem,
    )


T = TypeVar("T", bound="PermissionOptionsEnvelope")


@_attrs_define
class PermissionOptionsEnvelope:
    """Vocabulary of permission areas that may be granted to a contact or account manager, as key/label pairs. Returned by
    GET /contacts/permission-options and GET /managers/permission-options (the manager vocabulary is the contact
    vocabulary minus the _managed area).

        Attributes:
            permissions (list[PermissionOptionsEnvelopePermissionsItem]): Grantable permission areas. Keys mirror the
                portal's permission options, including any plugin-contributed areas. Example: [{'key': 'client_invoices',
                'label': 'Invoices'}, {'key': 'client_services', 'label': 'Services'}].
    """

    permissions: list[PermissionOptionsEnvelopePermissionsItem]

    def to_dict(self) -> dict[str, Any]:
        permissions = []
        for permissions_item_data in self.permissions:
            permissions_item = permissions_item_data.to_dict()
            permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.permission_options_envelope_permissions_item import (
            PermissionOptionsEnvelopePermissionsItem,
        )

        d = dict(src_dict)
        permissions = []
        _permissions = d.pop("permissions")
        for permissions_item_data in _permissions:
            permissions_item = PermissionOptionsEnvelopePermissionsItem.from_dict(
                permissions_item_data
            )

            permissions.append(permissions_item)

        permission_options_envelope = cls(
            permissions=permissions,
        )

        return permission_options_envelope
