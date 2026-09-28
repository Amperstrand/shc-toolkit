from enum import StrEnum


class GetContactResponse200DataNumbersItemLocation(StrEnum):
    HOME = "home"
    MOBILE = "mobile"
    WORK = "work"

    def __str__(self) -> str:
        return str(self.value)
