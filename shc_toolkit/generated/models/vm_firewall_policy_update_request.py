from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.vm_firewall_policy_update_request_policy_in import (
    VmFirewallPolicyUpdateRequestPolicyIn,
    check_vm_firewall_policy_update_request_policy_in,
)
from ..models.vm_firewall_policy_update_request_policy_out import (
    VmFirewallPolicyUpdateRequestPolicyOut,
    check_vm_firewall_policy_update_request_policy_out,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="VmFirewallPolicyUpdateRequest")


@_attrs_define
class VmFirewallPolicyUpdateRequest:
    """Set the default inbound/outbound firewall policy. PATCH semantics: only the keys present are set; at least one of
    policy_in/policy_out is required.

        Example:
            {'policy_in': 'DROP', 'policy_out': 'ACCEPT'}

    """

    policy_in: VmFirewallPolicyUpdateRequestPolicyIn | Unset = UNSET
    """ Default inbound policy. v2.4.0: case-INSENSITIVE on input (accept/Drop/REJECT all valid); always canonical
    UPPERCASE on output. """
    policy_out: VmFirewallPolicyUpdateRequestPolicyOut | Unset = UNSET
    """ Default outbound policy. v2.4.0: case-INSENSITIVE on input (accept/Drop/REJECT all valid); always canonical
    UPPERCASE on output. """

    def to_dict(self) -> dict[str, Any]:
        policy_in: str | Unset = UNSET
        if not isinstance(self.policy_in, Unset):
            policy_in = self.policy_in

        policy_out: str | Unset = UNSET
        if not isinstance(self.policy_out, Unset):
            policy_out = self.policy_out

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if policy_in is not UNSET:
            field_dict["policy_in"] = policy_in
        if policy_out is not UNSET:
            field_dict["policy_out"] = policy_out

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        _policy_in = d.pop("policy_in", UNSET)
        policy_in: VmFirewallPolicyUpdateRequestPolicyIn | Unset
        if isinstance(_policy_in, Unset):
            policy_in = UNSET
        else:
            policy_in = check_vm_firewall_policy_update_request_policy_in(_policy_in)

        _policy_out = d.pop("policy_out", UNSET)
        policy_out: VmFirewallPolicyUpdateRequestPolicyOut | Unset
        if isinstance(_policy_out, Unset):
            policy_out = UNSET
        else:
            policy_out = check_vm_firewall_policy_update_request_policy_out(_policy_out)

        vm_firewall_policy_update_request = cls(
            policy_in=policy_in,
            policy_out=policy_out,
        )

        return vm_firewall_policy_update_request
