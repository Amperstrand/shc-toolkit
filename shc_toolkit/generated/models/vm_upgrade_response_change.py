from typing import Literal

VmUpgradeResponseChange = Literal["queued"]

VM_UPGRADE_RESPONSE_CHANGE_VALUES: set[VmUpgradeResponseChange] = {
    "queued",
}


def check_vm_upgrade_response_change(value: str) -> VmUpgradeResponseChange:
    if value in VM_UPGRADE_RESPONSE_CHANGE_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_UPGRADE_RESPONSE_CHANGE_VALUES!r}"
    )
