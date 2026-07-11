from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vm_firewall_policy_response_policy import (
        VmFirewallPolicyResponsePolicy,
    )


T = TypeVar("T", bound="VmFirewallPolicyResponse")


@_attrs_define
class VmFirewallPolicyResponse:
    """The refreshed default firewall policy after an update.

    Attributes:
        service_id (int):  Example: 353.
        policy (VmFirewallPolicyResponsePolicy):
    """

    service_id: int
    policy: VmFirewallPolicyResponsePolicy
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        policy = self.policy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "policy": policy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vm_firewall_policy_response_policy import (
            VmFirewallPolicyResponsePolicy,
        )

        d = dict(src_dict)
        service_id = d.pop("service_id")

        policy = VmFirewallPolicyResponsePolicy.from_dict(d.pop("policy"))

        vm_firewall_policy_response = cls(
            service_id=service_id,
            policy=policy,
        )

        vm_firewall_policy_response.additional_properties = d
        return vm_firewall_policy_response

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
