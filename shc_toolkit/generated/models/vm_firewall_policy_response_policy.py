from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.vm_firewall_policy_response_policy_policy_in_type_1 import (
    VmFirewallPolicyResponsePolicyPolicyInType1,
    check_vm_firewall_policy_response_policy_policy_in_type_1,
)
from ..models.vm_firewall_policy_response_policy_policy_in_type_2_type_1 import (
    VmFirewallPolicyResponsePolicyPolicyInType2Type1,
    check_vm_firewall_policy_response_policy_policy_in_type_2_type_1,
)
from ..models.vm_firewall_policy_response_policy_policy_in_type_3_type_1 import (
    VmFirewallPolicyResponsePolicyPolicyInType3Type1,
    check_vm_firewall_policy_response_policy_policy_in_type_3_type_1,
)
from ..models.vm_firewall_policy_response_policy_policy_out_type_1 import (
    VmFirewallPolicyResponsePolicyPolicyOutType1,
    check_vm_firewall_policy_response_policy_policy_out_type_1,
)
from ..models.vm_firewall_policy_response_policy_policy_out_type_2_type_1 import (
    VmFirewallPolicyResponsePolicyPolicyOutType2Type1,
    check_vm_firewall_policy_response_policy_policy_out_type_2_type_1,
)
from ..models.vm_firewall_policy_response_policy_policy_out_type_3_type_1 import (
    VmFirewallPolicyResponsePolicyPolicyOutType3Type1,
    check_vm_firewall_policy_response_policy_policy_out_type_3_type_1,
)

T = TypeVar("T", bound="VmFirewallPolicyResponsePolicy")


@_attrs_define
class VmFirewallPolicyResponsePolicy:
    policy_in: (
        None
        | VmFirewallPolicyResponsePolicyPolicyInType1
        | VmFirewallPolicyResponsePolicyPolicyInType2Type1
        | VmFirewallPolicyResponsePolicyPolicyInType3Type1
    )
    policy_out: (
        None
        | VmFirewallPolicyResponsePolicyPolicyOutType1
        | VmFirewallPolicyResponsePolicyPolicyOutType2Type1
        | VmFirewallPolicyResponsePolicyPolicyOutType3Type1
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        policy_in: None | str
        if (
            isinstance(self.policy_in, str)
            or isinstance(self.policy_in, str)
            or isinstance(self.policy_in, str)
        ):
            policy_in = self.policy_in
        else:
            policy_in = self.policy_in

        policy_out: None | str
        if (
            isinstance(self.policy_out, str)
            or isinstance(self.policy_out, str)
            or isinstance(self.policy_out, str)
        ):
            policy_out = self.policy_out
        else:
            policy_out = self.policy_out

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy_in": policy_in,
                "policy_out": policy_out,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_policy_in(
            data: object,
        ) -> (
            None
            | VmFirewallPolicyResponsePolicyPolicyInType1
            | VmFirewallPolicyResponsePolicyPolicyInType2Type1
            | VmFirewallPolicyResponsePolicyPolicyInType3Type1
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_in_type_1 = (
                    check_vm_firewall_policy_response_policy_policy_in_type_1(data)
                )

                return policy_in_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_in_type_2_type_1 = (
                    check_vm_firewall_policy_response_policy_policy_in_type_2_type_1(
                        data
                    )
                )

                return policy_in_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_in_type_3_type_1 = (
                    check_vm_firewall_policy_response_policy_policy_in_type_3_type_1(
                        data
                    )
                )

                return policy_in_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | VmFirewallPolicyResponsePolicyPolicyInType1
                | VmFirewallPolicyResponsePolicyPolicyInType2Type1
                | VmFirewallPolicyResponsePolicyPolicyInType3Type1,
                data,
            )

        policy_in = _parse_policy_in(d.pop("policy_in"))

        def _parse_policy_out(
            data: object,
        ) -> (
            None
            | VmFirewallPolicyResponsePolicyPolicyOutType1
            | VmFirewallPolicyResponsePolicyPolicyOutType2Type1
            | VmFirewallPolicyResponsePolicyPolicyOutType3Type1
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_out_type_1 = (
                    check_vm_firewall_policy_response_policy_policy_out_type_1(data)
                )

                return policy_out_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_out_type_2_type_1 = (
                    check_vm_firewall_policy_response_policy_policy_out_type_2_type_1(
                        data
                    )
                )

                return policy_out_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_out_type_3_type_1 = (
                    check_vm_firewall_policy_response_policy_policy_out_type_3_type_1(
                        data
                    )
                )

                return policy_out_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | VmFirewallPolicyResponsePolicyPolicyOutType1
                | VmFirewallPolicyResponsePolicyPolicyOutType2Type1
                | VmFirewallPolicyResponsePolicyPolicyOutType3Type1,
                data,
            )

        policy_out = _parse_policy_out(d.pop("policy_out"))

        vm_firewall_policy_response_policy = cls(
            policy_in=policy_in,
            policy_out=policy_out,
        )

        vm_firewall_policy_response_policy.additional_properties = d
        return vm_firewall_policy_response_policy

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
