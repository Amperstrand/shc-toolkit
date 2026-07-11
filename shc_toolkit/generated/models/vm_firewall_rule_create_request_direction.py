from enum import Enum


class VmFirewallRuleCreateRequestDirection(str, Enum):
    IN = "in"
    OUT = "out"

    def __str__(self) -> str:
        return str(self.value)
