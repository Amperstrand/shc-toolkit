from enum import StrEnum


class UnlinkNostrIdentityResponse200DataStatus(StrEnum):
    UNLINKED = "unlinked"

    def __str__(self) -> str:
        return str(self.value)
