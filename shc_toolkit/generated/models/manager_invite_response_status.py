from enum import StrEnum


class ManagerInviteResponseStatus(StrEnum):
    INVALID = "invalid"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
