from typing import Literal

VmFirewallPolicyUpdateRequestPolicyOut = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_POLICY_UPDATE_REQUEST_POLICY_OUT_VALUES: set[
    VmFirewallPolicyUpdateRequestPolicyOut
] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_policy_update_request_policy_out(
    value: str,
) -> VmFirewallPolicyUpdateRequestPolicyOut:
    if value in VM_FIREWALL_POLICY_UPDATE_REQUEST_POLICY_OUT_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_POLICY_UPDATE_REQUEST_POLICY_OUT_VALUES!r}"
    )
