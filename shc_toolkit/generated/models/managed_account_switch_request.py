from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ManagedAccountSwitchRequest")


@_attrs_define
class ManagedAccountSwitchRequest:
    """Managed-account switch request. The requested areas are intersected with the Blesta-native manager grants; ungranted
    areas are rejected.

        Attributes:
            areas (list[str]): Requested effective areas. The server only switches into areas already granted to this
                manager on the target account.
    """

    areas: list[str]

    def to_dict(self) -> dict[str, Any]:
        areas = self.areas

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "areas": areas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        areas = cast(list[str], d.pop("areas"))

        managed_account_switch_request = cls(
            areas=areas,
        )

        return managed_account_switch_request
