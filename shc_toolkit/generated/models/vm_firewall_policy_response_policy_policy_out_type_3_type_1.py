from typing import Literal

VmFirewallPolicyResponsePolicyPolicyOutType3Type1 = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_POLICY_RESPONSE_POLICY_POLICY_OUT_TYPE_3_TYPE_1_VALUES: set[
    VmFirewallPolicyResponsePolicyPolicyOutType3Type1
] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_policy_response_policy_policy_out_type_3_type_1(
    value: str,
) -> VmFirewallPolicyResponsePolicyPolicyOutType3Type1:
    if value in VM_FIREWALL_POLICY_RESPONSE_POLICY_POLICY_OUT_TYPE_3_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_POLICY_RESPONSE_POLICY_POLICY_OUT_TYPE_3_TYPE_1_VALUES!r}"
    )
