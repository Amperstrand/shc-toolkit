from typing import Literal

VmFirewallPolicyPolicyOutType1 = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_POLICY_POLICY_OUT_TYPE_1_VALUES: set[VmFirewallPolicyPolicyOutType1] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_policy_policy_out_type_1(
    value: str,
) -> VmFirewallPolicyPolicyOutType1:
    if value in VM_FIREWALL_POLICY_POLICY_OUT_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_POLICY_POLICY_OUT_TYPE_1_VALUES!r}"
    )
