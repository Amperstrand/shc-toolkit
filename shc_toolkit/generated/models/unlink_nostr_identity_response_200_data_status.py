from enum import Enum


class UnlinkNostrIdentityResponse200DataStatus(str, Enum):
    UNLINKED = "unlinked"

    def __str__(self) -> str:
        return str(self.value)
