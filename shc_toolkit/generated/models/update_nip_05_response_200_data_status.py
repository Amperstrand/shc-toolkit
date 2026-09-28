from enum import StrEnum


class UpdateNip05Response200DataStatus(StrEnum):
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
