from enum import Enum


class VmFirewallPolicyResponsePolicyPolicyInType3Type1(str, Enum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"

    def __str__(self) -> str:
        return str(self.value)
