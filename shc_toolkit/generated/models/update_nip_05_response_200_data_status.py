from enum import Enum


class UpdateNip05Response200DataStatus(str, Enum):
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
