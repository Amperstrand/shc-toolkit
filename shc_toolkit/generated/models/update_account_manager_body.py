from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="UpdateAccountManagerBody")


@_attrs_define
class UpdateAccountManagerBody:
    """
    Attributes:
        permissions (list[str]): Required non-empty list of manager permission area keys.
    """

    permissions: list[str]

    def to_dict(self) -> dict[str, Any]:
        permissions = self.permissions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        permissions = cast(list[str], d.pop("permissions"))

        update_account_manager_body = cls(
            permissions=permissions,
        )

        return update_account_manager_body
