from typing import Literal

VmFirewallRuleCreateRequestAction = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_RULE_CREATE_REQUEST_ACTION_VALUES: set[
    VmFirewallRuleCreateRequestAction
] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_rule_create_request_action(
    value: str,
) -> VmFirewallRuleCreateRequestAction:
    if value in VM_FIREWALL_RULE_CREATE_REQUEST_ACTION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_RULE_CREATE_REQUEST_ACTION_VALUES!r}"
    )
