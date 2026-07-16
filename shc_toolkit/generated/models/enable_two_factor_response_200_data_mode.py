from enum import Enum


class EnableTwoFactorResponse200DataMode(str, Enum):
    NONE = "none"
    TOTP = "totp"

    def __str__(self) -> str:
        return str(self.value)
