from enum import StrEnum


class GetTwoFactorStatusResponse200DataMode(StrEnum):
    MOTP = "motp"
    NONE = "none"
    TOTP = "totp"

    def __str__(self) -> str:
        return str(self.value)
