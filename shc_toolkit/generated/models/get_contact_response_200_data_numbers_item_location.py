from enum import Enum


class GetContactResponse200DataNumbersItemLocation(str, Enum):
    HOME = "home"
    MOBILE = "mobile"
    WORK = "work"

    def __str__(self) -> str:
        return str(self.value)
