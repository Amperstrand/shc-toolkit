from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="UpdateAccountManagerResponse200Data")


@_attrs_define
class UpdateAccountManagerResponse200Data:
    updated: bool
    """ Whether the active manager permissions were updated. """
    contact_id: int
    """ Active manager contact id. """
    permissions: list[str]
    """ Permission area keys stored after the update. """

    def to_dict(self) -> dict[str, Any]:
        updated = self.updated

        contact_id = self.contact_id

        permissions = self.permissions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "updated": updated,
                "contact_id": contact_id,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        updated = d.pop("updated")

        contact_id = d.pop("contact_id")

        permissions = cast(list[str], d.pop("permissions"))

        update_account_manager_response_200_data = cls(
            updated=updated,
            contact_id=contact_id,
            permissions=permissions,
        )

        return update_account_manager_response_200_data
