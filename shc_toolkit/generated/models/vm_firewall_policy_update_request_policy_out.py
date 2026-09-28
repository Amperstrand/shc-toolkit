from enum import StrEnum


class VmFirewallPolicyUpdateRequestPolicyOut(StrEnum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"

    def __str__(self) -> str:
        return str(self.value)
