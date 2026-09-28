from enum import StrEnum


class VmFirewallRuleUpdateRequestAction(StrEnum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"

    def __str__(self) -> str:
        return str(self.value)
