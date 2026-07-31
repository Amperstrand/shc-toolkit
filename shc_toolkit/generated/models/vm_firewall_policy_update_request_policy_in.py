from typing import Literal

VmFirewallPolicyUpdateRequestPolicyIn = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_POLICY_UPDATE_REQUEST_POLICY_IN_VALUES: set[
    VmFirewallPolicyUpdateRequestPolicyIn
] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_policy_update_request_policy_in(
    value: str,
) -> VmFirewallPolicyUpdateRequestPolicyIn:
    if value in VM_FIREWALL_POLICY_UPDATE_REQUEST_POLICY_IN_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_POLICY_UPDATE_REQUEST_POLICY_IN_VALUES!r}"
    )
