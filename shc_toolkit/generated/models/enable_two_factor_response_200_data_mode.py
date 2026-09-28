from enum import StrEnum


class EnableTwoFactorResponse200DataMode(StrEnum):
    NONE = "none"
    TOTP = "totp"

    def __str__(self) -> str:
        return str(self.value)
