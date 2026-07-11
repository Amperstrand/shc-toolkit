from enum import Enum


class VmUpgradeOptionsResponseBlockedReasonType3Type1(str, Enum):
    CHANGE_NOT_ALLOWED = "change_not_allowed"
    NOT_ACTIVE = "not_active"
    PENDING_CHANGE = "pending_change"
    UNPAID_INVOICES = "unpaid_invoices"

    def __str__(self) -> str:
        return str(self.value)
