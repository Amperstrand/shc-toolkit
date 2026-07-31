from typing import Literal

VmFirewallPolicyPolicyInType3Type1 = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_POLICY_POLICY_IN_TYPE_3_TYPE_1_VALUES: set[
    VmFirewallPolicyPolicyInType3Type1
] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_policy_policy_in_type_3_type_1(
    value: str,
) -> VmFirewallPolicyPolicyInType3Type1:
    if value in VM_FIREWALL_POLICY_POLICY_IN_TYPE_3_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_POLICY_POLICY_IN_TYPE_3_TYPE_1_VALUES!r}"
    )
