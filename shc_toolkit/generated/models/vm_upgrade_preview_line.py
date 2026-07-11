from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmUpgradePreviewLine")


@_attrs_define
class VmUpgradePreviewLine:
    """
    Attributes:
        description (str | Unset):  Example: SSD VPS - Professional (Jun 7, 2026 - Jul 7, 2026).
        qty (float | Unset):  Example: 1.
        amount (str | Unset): Line amount. Example: 20.00.
    """

    description: str | Unset = UNSET
    qty: float | Unset = UNSET
    amount: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        qty = self.qty

        amount = self.amount

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if qty is not UNSET:
            field_dict["qty"] = qty
        if amount is not UNSET:
            field_dict["amount"] = amount

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        qty = d.pop("qty", UNSET)

        amount = d.pop("amount", UNSET)

        vm_upgrade_preview_line = cls(
            description=description,
            qty=qty,
            amount=amount,
        )

        vm_upgrade_preview_line.additional_properties = d
        return vm_upgrade_preview_line

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
