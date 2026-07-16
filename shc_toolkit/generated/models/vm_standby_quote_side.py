from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="VmStandbyQuoteSide")


@_attrs_define
class VmStandbyQuoteSide:
    """
    Attributes:
        recurring (str):  Example: 6.8340.
        credit (str):  Example: 51.9194.
    """

    recurring: str
    credit: str

    def to_dict(self) -> dict[str, Any]:
        recurring = self.recurring

        credit = self.credit

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "recurring": recurring,
                "credit": credit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recurring = d.pop("recurring")

        credit = d.pop("credit")

        vm_standby_quote_side = cls(
            recurring=recurring,
            credit=credit,
        )

        return vm_standby_quote_side
