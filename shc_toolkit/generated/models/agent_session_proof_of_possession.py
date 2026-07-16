from enum import Enum


class AgentSessionProofOfPossession(str, Enum):
    NONE = "none"
    NOSTR = "nostr"

    def __str__(self) -> str:
        return str(self.value)
