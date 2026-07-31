from typing import Literal

VmFirewallRuleUpdateRequestDirection = Literal["in", "out"]

VM_FIREWALL_RULE_UPDATE_REQUEST_DIRECTION_VALUES: set[
    VmFirewallRuleUpdateRequestDirection
] = {
    "in",
    "out",
}


def check_vm_firewall_rule_update_request_direction(
    value: str,
) -> VmFirewallRuleUpdateRequestDirection:
    if value in VM_FIREWALL_RULE_UPDATE_REQUEST_DIRECTION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_RULE_UPDATE_REQUEST_DIRECTION_VALUES!r}"
    )
