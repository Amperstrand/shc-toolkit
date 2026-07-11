from enum import Enum


class VmFirewallRuleUpdateRequestDirection(str, Enum):
    IN = "in"
    OUT = "out"

    def __str__(self) -> str:
        return str(self.value)
