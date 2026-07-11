from enum import Enum


class GetVirtualMachineBandwidthResponse200DataCountDirection(str, Enum):
    BOTH = "both"
    INBOUND = "inbound"
    OUTBOUND = "outbound"

    def __str__(self) -> str:
        return str(self.value)
