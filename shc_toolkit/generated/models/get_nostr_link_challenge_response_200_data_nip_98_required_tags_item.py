from enum import StrEnum


class GetNostrLinkChallengeResponse200DataNip98RequiredTagsItem(StrEnum):
    CHALLENGE = "challenge"
    METHOD = "method"
    U = "u"

    def __str__(self) -> str:
        return str(self.value)
