from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vm_firewall_actions_item import VmFirewallActionsItem
from ..models.vm_firewall_directions_item import VmFirewallDirectionsItem

if TYPE_CHECKING:
    from ..models.vm_firewall_macros_item import VmFirewallMacrosItem
    from ..models.vm_firewall_policy import VmFirewallPolicy
    from ..models.vm_firewall_rule import VmFirewallRule


T = TypeVar("T", bound="VmFirewall")


@_attrs_define
class VmFirewall:
    """Per-VM firewall configuration and rule-form vocabulary.

    Attributes:
        service_id (int): Owned Blesta service id.
        policy (VmFirewallPolicy): Default firewall policy.
        rules (list[VmFirewallRule]): Firewall rules (security-group rules are excluded).
        interfaces (list[str]): VM network interface keys (e.g. net0) selectable on a rule.
        macros (list[VmFirewallMacrosItem]): Available firewall macros.
        directions (list[VmFirewallDirectionsItem]): Supported rule directions.
        actions (list[VmFirewallActionsItem]): Supported rule actions.
        icmp_types (list[str]): Supported ICMP types for ICMP rules.
    """

    service_id: int
    policy: VmFirewallPolicy
    rules: list[VmFirewallRule]
    interfaces: list[str]
    macros: list[VmFirewallMacrosItem]
    directions: list[VmFirewallDirectionsItem]
    actions: list[VmFirewallActionsItem]
    icmp_types: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        policy = self.policy.to_dict()

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        interfaces = self.interfaces

        macros = []
        for macros_item_data in self.macros:
            macros_item = macros_item_data.to_dict()
            macros.append(macros_item)

        directions = []
        for directions_item_data in self.directions:
            directions_item = directions_item_data.value
            directions.append(directions_item)

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.value
            actions.append(actions_item)

        icmp_types = self.icmp_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "policy": policy,
                "rules": rules,
                "interfaces": interfaces,
                "macros": macros,
                "directions": directions,
                "actions": actions,
                "icmp_types": icmp_types,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_firewall_macros_item import VmFirewallMacrosItem
        from ..models.vm_firewall_policy import VmFirewallPolicy
        from ..models.vm_firewall_rule import VmFirewallRule

        d = dict(src_dict)
        service_id = d.pop("service_id")

        policy = VmFirewallPolicy.from_dict(d.pop("policy"))

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = VmFirewallRule.from_dict(rules_item_data)

            rules.append(rules_item)

        interfaces = cast(list[str], d.pop("interfaces"))

        macros = []
        _macros = d.pop("macros")
        for macros_item_data in _macros:
            macros_item = VmFirewallMacrosItem.from_dict(macros_item_data)

            macros.append(macros_item)

        directions = []
        _directions = d.pop("directions")
        for directions_item_data in _directions:
            directions_item = VmFirewallDirectionsItem(directions_item_data)

            directions.append(directions_item)

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = VmFirewallActionsItem(actions_item_data)

            actions.append(actions_item)

        icmp_types = cast(list[str], d.pop("icmp_types"))

        vm_firewall = cls(
            service_id=service_id,
            policy=policy,
            rules=rules,
            interfaces=interfaces,
            macros=macros,
            directions=directions,
            actions=actions,
            icmp_types=icmp_types,
        )

        vm_firewall.additional_properties = d
        return vm_firewall

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
