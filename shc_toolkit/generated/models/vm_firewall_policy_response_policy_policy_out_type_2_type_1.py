from enum import StrEnum


class VmFirewallPolicyResponsePolicyPolicyOutType2Type1(StrEnum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"

    def __str__(self) -> str:
        return str(self.value)
