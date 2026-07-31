from typing import Literal

VmFirewallActionsItem = Literal["ACCEPT", "DROP", "REJECT"]

VM_FIREWALL_ACTIONS_ITEM_VALUES: set[VmFirewallActionsItem] = {
    "ACCEPT",
    "DROP",
    "REJECT",
}


def check_vm_firewall_actions_item(value: str) -> VmFirewallActionsItem:
    if value in VM_FIREWALL_ACTIONS_ITEM_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_ACTIONS_ITEM_VALUES!r}"
    )
