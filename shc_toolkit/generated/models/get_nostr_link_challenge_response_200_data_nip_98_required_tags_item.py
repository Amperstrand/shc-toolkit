from enum import Enum


class GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem(str, Enum):
    CHALLENGE = "challenge"
    METHOD = "method"
    U = "u"

    def __str__(self) -> str:
        return str(self.value)
