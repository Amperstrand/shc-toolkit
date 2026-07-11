from enum import Enum


class ManagerDeleteResponseStatus(str, Enum):
    DECLINED = "declined"

    def __str__(self) -> str:
        return str(self.value)
