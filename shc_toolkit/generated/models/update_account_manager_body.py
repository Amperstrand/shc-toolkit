from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateAccountManagerBody")


@_attrs_define
class UpdateAccountManagerBody:
    """
    Attributes:
        permissions (list[str] | Unset):
        status (str | Unset):
        note (str | Unset):
    """

    permissions: list[str] | Unset = UNSET
    status: str | Unset = UNSET
    note: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        permissions: list[str] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        status = self.status

        note = self.note

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if status is not UNSET:
            field_dict["status"] = status
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        permissions = cast(list[str], d.pop("permissions", UNSET))

        status = d.pop("status", UNSET)

        note = d.pop("note", UNSET)

        update_account_manager_body = cls(
            permissions=permissions,
            status=status,
            note=note,
        )

        return update_account_manager_body
