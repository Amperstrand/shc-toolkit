from enum import StrEnum


class VmFirewallPolicyResponsePolicyPolicyOutType1(StrEnum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"

    def __str__(self) -> str:
        return str(self.value)
