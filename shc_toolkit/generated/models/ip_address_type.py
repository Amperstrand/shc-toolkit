from enum import Enum


class IpAddressType(str, Enum):
    V4 = "v4"
    V6 = "v6"

    def __str__(self) -> str:
        return str(self.value)
