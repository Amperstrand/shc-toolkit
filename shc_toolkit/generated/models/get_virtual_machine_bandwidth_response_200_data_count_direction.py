from enum import StrEnum


class GetVirtualMachineBandwidthResponse200DataCountDirection(StrEnum):
    BOTH = "both"
    INBOUND = "inbound"
    OUTBOUND = "outbound"

    def __str__(self) -> str:
        return str(self.value)
