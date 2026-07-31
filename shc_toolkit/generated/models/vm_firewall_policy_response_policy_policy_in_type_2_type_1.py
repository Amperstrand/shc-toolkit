from typing import Literal

VmFirewallPolicyResponsePolicyPolicyInType2Type1 = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_POLICY_RESPONSE_POLICY_POLICY_IN_TYPE_2_TYPE_1_VALUES: set[
    VmFirewallPolicyResponsePolicyPolicyInType2Type1
] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_policy_response_policy_policy_in_type_2_type_1(
    value: str,
) -> VmFirewallPolicyResponsePolicyPolicyInType2Type1:
    if value in VM_FIREWALL_POLICY_RESPONSE_POLICY_POLICY_IN_TYPE_2_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_POLICY_RESPONSE_POLICY_POLICY_IN_TYPE_2_TYPE_1_VALUES!r}"
    )
