from typing import Literal

VmUpgradeOptionsResponseBlockedReasonType3Type1 = Literal[
    "change_not_allowed", "not_active", "pending_change", "unpaid_invoices"
]

VM_UPGRADE_OPTIONS_RESPONSE_BLOCKED_REASON_TYPE_3_TYPE_1_VALUES: set[
    VmUpgradeOptionsResponseBlockedReasonType3Type1
] = {
    "change_not_allowed",
    "not_active",
    "pending_change",
    "unpaid_invoices",
}


def check_vm_upgrade_options_response_blocked_reason_type_3_type_1(
    value: str,
) -> VmUpgradeOptionsResponseBlockedReasonType3Type1:
    if value in VM_UPGRADE_OPTIONS_RESPONSE_BLOCKED_REASON_TYPE_3_TYPE_1_VALUES:
        return value
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {VM_UPGRADE_OPTIONS_RESPONSE_BLOCKED_REASON_TYPE_3_TYPE_1_VALUES!r}"
    )
