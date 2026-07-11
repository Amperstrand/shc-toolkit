from enum import Enum


class GetTwoFactorStatusResponse200DataMode(str, Enum):
    MOTP = "motp"
    NONE = "none"
    TOTP = "totp"

    def __str__(self) -> str:
        return str(self.value)
