from enum import Enum


class GetContactResponse200DataNumbersItemType(str, Enum):
    FAX = "fax"
    PHONE = "phone"

    def __str__(self) -> str:
        return str(self.value)
