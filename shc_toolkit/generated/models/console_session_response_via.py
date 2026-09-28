from enum import StrEnum


class ConsoleSessionResponseVia(StrEnum):
    SECURE_BRIDGE_JWT = "secure_bridge_jwt"

    def __str__(self) -> str:
        return str(self.value)
