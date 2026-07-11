from enum import Enum


class VmFirewallPolicyResponsePolicyPolicyOutType3Type1(str, Enum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"

    def __str__(self) -> str:
        return str(self.value)
