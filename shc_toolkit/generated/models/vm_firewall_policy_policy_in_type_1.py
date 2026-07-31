from typing import Literal

VmFirewallPolicyPolicyInType1 = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_POLICY_POLICY_IN_TYPE_1_VALUES: set[VmFirewallPolicyPolicyInType1] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_policy_policy_in_type_1(
    value: str,
) -> VmFirewallPolicyPolicyInType1:
    if value in VM_FIREWALL_POLICY_POLICY_IN_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_POLICY_POLICY_IN_TYPE_1_VALUES!r}"
    )
