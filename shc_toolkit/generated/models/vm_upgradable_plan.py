from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_upgradable_plan_available_config_options_item import (
        VmUpgradablePlanAvailableConfigOptionsItem,
    )
    from ..models.vm_upgrade_option_term import VmUpgradeOptionTerm


T = TypeVar("T", bound="VmUpgradablePlan")


@_attrs_define
class VmUpgradablePlan:
    """A same-group package the service may move to. disk_reduces / disk_change_blocked flag a base-disk-shrinking move
    (rejected at commit). Placement is never present.

        Attributes:
            plan_label (str):  Example: SSD VPS - Professional.
            terms (list[VmUpgradeOptionTerm]):
            cpu (int | None | Unset):  Example: 4.
            memory_mb (int | None | Unset):  Example: 16384.
            disk_gb (int | None | Unset): Base package disk (GB), config options excluded. Example: 32.
            available_config_options (list[VmUpgradablePlanAvailableConfigOptionsItem] | Unset): Catalog of settable config
                options per term (ordering catalog shape).
            disk_reduces (bool | Unset): True if a no-add-on move to this plan would reduce disk.
            disk_change_blocked (bool | Unset): True if a disk-reducing move is rejected at commit.
    """

    plan_label: str
    terms: list[VmUpgradeOptionTerm]
    cpu: int | None | Unset = UNSET
    memory_mb: int | None | Unset = UNSET
    disk_gb: int | None | Unset = UNSET
    available_config_options: (
        list[VmUpgradablePlanAvailableConfigOptionsItem] | Unset
    ) = UNSET
    disk_reduces: bool | Unset = UNSET
    disk_change_blocked: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan_label = self.plan_label

        terms = []
        for terms_item_data in self.terms:
            terms_item = terms_item_data.to_dict()
            terms.append(terms_item)

        cpu: int | None | Unset
        if isinstance(self.cpu, Unset):
            cpu = UNSET
        else:
            cpu = self.cpu

        memory_mb: int | None | Unset
        if isinstance(self.memory_mb, Unset):
            memory_mb = UNSET
        else:
            memory_mb = self.memory_mb

        disk_gb: int | None | Unset
        if isinstance(self.disk_gb, Unset):
            disk_gb = UNSET
        else:
            disk_gb = self.disk_gb

        available_config_options: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.available_config_options, Unset):
            available_config_options = []
            for available_config_options_item_data in self.available_config_options:
                available_config_options_item = (
                    available_config_options_item_data.to_dict()
                )
                available_config_options.append(available_config_options_item)

        disk_reduces = self.disk_reduces

        disk_change_blocked = self.disk_change_blocked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan_label": plan_label,
                "terms": terms,
            }
        )
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if memory_mb is not UNSET:
            field_dict["memory_mb"] = memory_mb
        if disk_gb is not UNSET:
            field_dict["disk_gb"] = disk_gb
        if available_config_options is not UNSET:
            field_dict["available_config_options"] = available_config_options
        if disk_reduces is not UNSET:
            field_dict["disk_reduces"] = disk_reduces
        if disk_change_blocked is not UNSET:
            field_dict["disk_change_blocked"] = disk_change_blocked

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_upgradable_plan_available_config_options_item import (
            VmUpgradablePlanAvailableConfigOptionsItem,
        )
        from ..models.vm_upgrade_option_term import VmUpgradeOptionTerm

        d = dict(src_dict)
        plan_label = d.pop("plan_label")

        terms = []
        _terms = d.pop("terms")
        for terms_item_data in _terms:
            terms_item = VmUpgradeOptionTerm.from_dict(terms_item_data)

            terms.append(terms_item)

        def _parse_cpu(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cpu = _parse_cpu(d.pop("cpu", UNSET))

        def _parse_memory_mb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        memory_mb = _parse_memory_mb(d.pop("memory_mb", UNSET))

        def _parse_disk_gb(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        disk_gb = _parse_disk_gb(d.pop("disk_gb", UNSET))

        _available_config_options = d.pop("available_config_options", UNSET)
        available_config_options: (
            list[VmUpgradablePlanAvailableConfigOptionsItem] | Unset
        ) = UNSET
        if _available_config_options is not UNSET:
            available_config_options = []
            for available_config_options_item_data in _available_config_options:
                available_config_options_item = (
                    VmUpgradablePlanAvailableConfigOptionsItem.from_dict(
                        available_config_options_item_data
                    )
                )

                available_config_options.append(available_config_options_item)

        disk_reduces = d.pop("disk_reduces", UNSET)

        disk_change_blocked = d.pop("disk_change_blocked", UNSET)

        vm_upgradable_plan = cls(
            plan_label=plan_label,
            terms=terms,
            cpu=cpu,
            memory_mb=memory_mb,
            disk_gb=disk_gb,
            available_config_options=available_config_options,
            disk_reduces=disk_reduces,
            disk_change_blocked=disk_change_blocked,
        )

        vm_upgradable_plan.additional_properties = d
        return vm_upgradable_plan

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
