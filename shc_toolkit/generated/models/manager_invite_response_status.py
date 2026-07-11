from enum import Enum


class ManagerInviteResponseStatus(str, Enum):
    INVALID = "invalid"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
