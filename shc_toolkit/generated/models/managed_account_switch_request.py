from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="ManagedAccountSwitchRequest")


@_attrs_define
class ManagedAccountSwitchRequest:
    """Managed-account switch request. The requested areas are intersected with the Blesta-native manager grants; ungranted
    areas are rejected.

    """

    areas: list[str]
    """ Requested effective areas. The server only switches into areas already granted to this manager on the target
    account. """

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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        areas = cast(list[str], d.pop("areas"))

        managed_account_switch_request = cls(
            areas=areas,
        )

        return managed_account_switch_request
