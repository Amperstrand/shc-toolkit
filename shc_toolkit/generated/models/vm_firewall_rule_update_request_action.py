from typing import Literal

VmFirewallRuleUpdateRequestAction = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_RULE_UPDATE_REQUEST_ACTION_VALUES: set[
    VmFirewallRuleUpdateRequestAction
] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_rule_update_request_action(
    value: str,
) -> VmFirewallRuleUpdateRequestAction:
    if value in VM_FIREWALL_RULE_UPDATE_REQUEST_ACTION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_RULE_UPDATE_REQUEST_ACTION_VALUES!r}"
    )
