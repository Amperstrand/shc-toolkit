from typing import Literal

VmFirewallRuleCreateRequestDirection = Literal["in", "out"]

VM_FIREWALL_RULE_CREATE_REQUEST_DIRECTION_VALUES: set[
    VmFirewallRuleCreateRequestDirection
] = {
    "in",
    "out",
}


def check_vm_firewall_rule_create_request_direction(
    value: str,
) -> VmFirewallRuleCreateRequestDirection:
    if value in VM_FIREWALL_RULE_CREATE_REQUEST_DIRECTION_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_RULE_CREATE_REQUEST_DIRECTION_VALUES!r}"
    )
