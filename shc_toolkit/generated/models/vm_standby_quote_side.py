from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

T = TypeVar("T", bound="VmStandbyQuoteSide")


@_attrs_define
class VmStandbyQuoteSide:
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
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        recurring = d.pop("recurring")

        credit = d.pop("credit")

        vm_standby_quote_side = cls(
            recurring=recurring,
            credit=credit,
        )

        return vm_standby_quote_side
