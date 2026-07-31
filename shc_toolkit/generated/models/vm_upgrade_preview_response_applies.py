from typing import Literal

VmUpgradePreviewResponseApplies = Literal["queued"]

VM_UPGRADE_PREVIEW_RESPONSE_APPLIES_VALUES: set[VmUpgradePreviewResponseApplies] = {
    "queued",
}


def check_vm_upgrade_preview_response_applies(
    value: str,
) -> VmUpgradePreviewResponseApplies:
    if value in VM_UPGRADE_PREVIEW_RESPONSE_APPLIES_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_UPGRADE_PREVIEW_RESPONSE_APPLIES_VALUES!r}"
    )
