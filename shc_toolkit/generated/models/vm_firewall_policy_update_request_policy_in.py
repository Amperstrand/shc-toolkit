from enum import Enum


class VmFirewallPolicyUpdateRequestPolicyIn(str, Enum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"

    def __str__(self) -> str:
        return str(self.value)
