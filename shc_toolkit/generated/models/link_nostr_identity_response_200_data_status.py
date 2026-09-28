from enum import StrEnum


class LinkNostrIdentityResponse200DataStatus(StrEnum):
    ALREADY_LINKED = "already_linked"
    LINKED = "linked"

    def __str__(self) -> str:
        return str(self.value)
