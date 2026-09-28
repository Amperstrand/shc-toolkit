from enum import StrEnum


class AgentSessionProofOfPossession(StrEnum):
    NONE = "none"
    NOSTR = "nostr"

    def __str__(self) -> str:
        return str(self.value)
