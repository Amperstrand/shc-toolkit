from enum import StrEnum


class ManagerDeleteResponseStatus(StrEnum):
    DECLINED = "declined"

    def __str__(self) -> str:
        return str(self.value)
