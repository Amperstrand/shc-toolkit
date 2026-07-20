from enum import Enum


class LinkNostrIdentityResponse200DataStatus(str, Enum):
    ALREADY_LINKED = "already_linked"
    LINKED = "linked"

    def __str__(self) -> str:
        return str(self.value)
