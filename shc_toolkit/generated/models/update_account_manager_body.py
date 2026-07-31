from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="UpdateAccountManagerBody")


@_attrs_define
class UpdateAccountManagerBody:
    permissions: list[str]
    """ Required non-empty list of manager permission area keys. """

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        permissions = cast(list[str], d.pop("permissions"))

        update_account_manager_body = cls(
            permissions=permissions,
        )

        return update_account_manager_body
