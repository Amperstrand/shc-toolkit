from typing import Literal

VmUpgradeOptionsResponseBlockedReasonType2Type1 = Literal[
    "change_not_allowed", "not_active", "pending_change", "unpaid_invoices"
]

VM_UPGRADE_OPTIONS_RESPONSE_BLOCKED_REASON_TYPE_2_TYPE_1_VALUES: set[
    VmUpgradeOptionsResponseBlockedReasonType2Type1
] = {
    "change_not_allowed",
    "not_active",
    "pending_change",
    "unpaid_invoices",
}


def check_vm_upgrade_options_response_blocked_reason_type_2_type_1(
    value: str,
) -> VmUpgradeOptionsResponseBlockedReasonType2Type1:
    if value in VM_UPGRADE_OPTIONS_RESPONSE_BLOCKED_REASON_TYPE_2_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_UPGRADE_OPTIONS_RESPONSE_BLOCKED_REASON_TYPE_2_TYPE_1_VALUES!r}"
    )
