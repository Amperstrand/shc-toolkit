from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AccountPasswordChangeResponse")


@_attrs_define
class AccountPasswordChangeResponse:
    """
    Attributes:
        password_changed_at (datetime.datetime):  Example: 2026-05-05T23:15:42+00:00.
    """

    password_changed_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        password_changed_at = self.password_changed_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "password_changed_at": password_changed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        password_changed_at = datetime.datetime.fromisoformat(
            d.pop("password_changed_at")
        )

        account_password_change_response = cls(
            password_changed_at=password_changed_at,
        )

        return account_password_change_response
