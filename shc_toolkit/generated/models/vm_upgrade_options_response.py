from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vm_upgrade_options_response_blocked_reason_type_1 import (
    VmUpgradeOptionsResponseBlockedReasonType1,
)
from ..models.vm_upgrade_options_response_blocked_reason_type_2_type_1 import (
    VmUpgradeOptionsResponseBlockedReasonType2Type1,
)
from ..models.vm_upgrade_options_response_blocked_reason_type_3_type_1 import (
    VmUpgradeOptionsResponseBlockedReasonType3Type1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vm_upgradable_plan import VmUpgradablePlan
    from ..models.vm_upgrade_options_response_current import (
        VmUpgradeOptionsResponseCurrent,
    )


T = TypeVar("T", bound="VmUpgradeOptionsResponse")


@_attrs_define
class VmUpgradeOptionsResponse:
    """The current plan + the same-group plans the customer may move to, with a blocked_reason when a change cannot
    proceed. Placement is never exposed.

        Attributes:
            service_id (int):  Example: 456.
            current (VmUpgradeOptionsResponseCurrent):
            upgradable (list[VmUpgradablePlan]):
            change_package_allowed (bool):  Example: True.
            change_term_allowed (bool):
            blocked_reason (None | VmUpgradeOptionsResponseBlockedReasonType1 |
                VmUpgradeOptionsResponseBlockedReasonType2Type1 | VmUpgradeOptionsResponseBlockedReasonType3Type1): Why a change
                cannot proceed right now, or null.
            items (list[VmUpgradablePlan] | Unset): v2.4.0 alias (additive): identical to 'upgradable' (the generic list
                key).
    """

    service_id: int
    current: VmUpgradeOptionsResponseCurrent
    upgradable: list[VmUpgradablePlan]
    change_package_allowed: bool
    change_term_allowed: bool
    blocked_reason: (
        None
        | VmUpgradeOptionsResponseBlockedReasonType1
        | VmUpgradeOptionsResponseBlockedReasonType2Type1
        | VmUpgradeOptionsResponseBlockedReasonType3Type1
    )
    items: list[VmUpgradablePlan] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        current = self.current.to_dict()

        upgradable = []
        for upgradable_item_data in self.upgradable:
            upgradable_item = upgradable_item_data.to_dict()
            upgradable.append(upgradable_item)

        change_package_allowed = self.change_package_allowed

        change_term_allowed = self.change_term_allowed

        blocked_reason: None | str
        if isinstance(self.blocked_reason, VmUpgradeOptionsResponseBlockedReasonType1):
            blocked_reason = self.blocked_reason.value
        elif isinstance(
            self.blocked_reason, VmUpgradeOptionsResponseBlockedReasonType2Type1
        ):
            blocked_reason = self.blocked_reason.value
        elif isinstance(
            self.blocked_reason, VmUpgradeOptionsResponseBlockedReasonType3Type1
        ):
            blocked_reason = self.blocked_reason.value
        else:
            blocked_reason = self.blocked_reason

        items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "current": current,
                "upgradable": upgradable,
                "change_package_allowed": change_package_allowed,
                "change_term_allowed": change_term_allowed,
                "blocked_reason": blocked_reason,
            }
        )
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_upgradable_plan import VmUpgradablePlan
        from ..models.vm_upgrade_options_response_current import (
            VmUpgradeOptionsResponseCurrent,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        current = VmUpgradeOptionsResponseCurrent.from_dict(d.pop("current"))

        upgradable = []
        _upgradable = d.pop("upgradable")
        for upgradable_item_data in _upgradable:
            upgradable_item = VmUpgradablePlan.from_dict(upgradable_item_data)

            upgradable.append(upgradable_item)

        change_package_allowed = d.pop("change_package_allowed")

        change_term_allowed = d.pop("change_term_allowed")

        def _parse_blocked_reason(
            data: object,
        ) -> (
            None
            | VmUpgradeOptionsResponseBlockedReasonType1
            | VmUpgradeOptionsResponseBlockedReasonType2Type1
            | VmUpgradeOptionsResponseBlockedReasonType3Type1
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                blocked_reason_type_1 = VmUpgradeOptionsResponseBlockedReasonType1(data)

                return blocked_reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                blocked_reason_type_2_type_1 = (
                    VmUpgradeOptionsResponseBlockedReasonType2Type1(data)
                )

                return blocked_reason_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                blocked_reason_type_3_type_1 = (
                    VmUpgradeOptionsResponseBlockedReasonType3Type1(data)
                )

                return blocked_reason_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | VmUpgradeOptionsResponseBlockedReasonType1
                | VmUpgradeOptionsResponseBlockedReasonType2Type1
                | VmUpgradeOptionsResponseBlockedReasonType3Type1,
                data,
            )

        blocked_reason = _parse_blocked_reason(d.pop("blocked_reason"))

        _items = d.pop("items", UNSET)
        items: list[VmUpgradablePlan] | Unset = UNSET
        if _items is not UNSET:
            items = []
            for items_item_data in _items:
                items_item = VmUpgradablePlan.from_dict(items_item_data)

                items.append(items_item)

        vm_upgrade_options_response = cls(
            service_id=service_id,
            current=current,
            upgradable=upgradable,
            change_package_allowed=change_package_allowed,
            change_term_allowed=change_term_allowed,
            blocked_reason=blocked_reason,
            items=items,
        )

        vm_upgrade_options_response.additional_properties = d
        return vm_upgrade_options_response

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
