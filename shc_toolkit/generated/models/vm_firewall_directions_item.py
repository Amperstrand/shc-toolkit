from typing import Literal

VmFirewallDirectionsItem = Literal["in", "out"]

VM_FIREWALL_DIRECTIONS_ITEM_VALUES: set[VmFirewallDirectionsItem] = {
    "in",
    "out",
}


def check_vm_firewall_directions_item(value: str) -> VmFirewallDirectionsItem:
    if value in VM_FIREWALL_DIRECTIONS_ITEM_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_FIREWALL_DIRECTIONS_ITEM_VALUES!r}"
    )
