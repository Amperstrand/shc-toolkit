from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_firewall_rule import VmFirewallRule


T = TypeVar("T", bound="VmFirewallRuleListResponse")


@_attrs_define
class VmFirewallRuleListResponse:
    """The refreshed client-visible firewall rule list after a rule mutation (security-group rules excluded).

    Attributes:
        service_id (int):  Example: 353.
        rules (list[VmFirewallRule]):
    """

    service_id: int
    rules: list[VmFirewallRule]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "rules": rules,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_firewall_rule import VmFirewallRule

        d = dict(src_dict)
        service_id = d.pop("service_id")

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = VmFirewallRule.from_dict(rules_item_data)

            rules.append(rules_item)

        vm_firewall_rule_list_response = cls(
            service_id=service_id,
            rules=rules,
        )

        vm_firewall_rule_list_response.additional_properties = d
        return vm_firewall_rule_list_response

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
