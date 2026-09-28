from enum import IntEnum


class GetNostrLinkChallengeResponse200DataExpiresInSeconds(IntEnum):
    VALUE_300 = 300

    def __str__(self) -> str:
        return str(self.value)
