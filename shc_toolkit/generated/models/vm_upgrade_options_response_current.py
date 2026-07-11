from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VmUpgradeOptionsResponseCurrent")


@_attrs_define
class VmUpgradeOptionsResponseCurrent:
    """
    Attributes:
        plan_label (str | Unset):  Example: SSD VPS - Standard.
        term (int | Unset):  Example: 1.
        period (str | Unset):  Example: month.
        recurring_amount (str | Unset): Current recurring price. Example: 12.00.
        currency (str | Unset):  Example: USD.
        disk_gb (int | None | Unset): Current effective disk (base meta + current disk options). Example: 16.
    """

    plan_label: str | Unset = UNSET
    term: int | Unset = UNSET
    period: str | Unset = UNSET
    recurring_amount: str | Unset = UNSET
    currency: str | Unset = UNSET
    disk_gb: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan_label = self.plan_label

        term = self.term

        period = self.period

        recurring_amount = self.recurring_amount

        currency = self.currency

        disk_gb: int | None | Unset
        if isinstance(self.disk_gb, Unset):
            disk_gb = UNSET
        else:
            disk_gb = self.disk_gb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plan_label is not UNSET:
            field_dict["plan_label"] = plan_label
        if term is not UNSET:
            field_dict["term"] = term
        if period is not UNSET:
            field_dict["period"] = period
        if recurring_amount is not UNSET:
            field_dict["recurring_amount"] = recurring_amount
        if currency is not UNSET:
            field_dict["currency"] = currency
        if disk_gb is not UNSET:
            field_dict["disk_gb"] = disk_gb

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plan_label = d.pop("plan_label", UNSET)

        term = d.pop("term", UNSET)

        period = d.pop("period", UNSET)

        recurring_amount = d.pop("recurring_amount", UNSET)

        currency = d.pop("currency", UNSET)

        def _parse_disk_gb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        disk_gb = _parse_disk_gb(d.pop("disk_gb", UNSET))

        vm_upgrade_options_response_current = cls(
            plan_label=plan_label,
            term=term,
            period=period,
            recurring_amount=recurring_amount,
            currency=currency,
            disk_gb=disk_gb,
        )

        vm_upgrade_options_response_current.additional_properties = d
        return vm_upgrade_options_response_current

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
