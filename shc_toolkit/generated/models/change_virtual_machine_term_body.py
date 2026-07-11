from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangeVirtualMachineTermBody")


@_attrs_define
class ChangeVirtualMachineTermBody:
    """
    Attributes:
        term_id (str):
        effective_at (str | Unset):
    """

    term_id: str
    effective_at: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        term_id = self.term_id

        effective_at = self.effective_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "termId": term_id,
            }
        )
        if effective_at is not UNSET:
            field_dict["effectiveAt"] = effective_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        term_id = d.pop("termId")

        effective_at = d.pop("effectiveAt", UNSET)

        change_virtual_machine_term_body = cls(
            term_id=term_id,
            effective_at=effective_at,
        )

        return change_virtual_machine_term_body
