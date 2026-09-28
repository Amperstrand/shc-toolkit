from enum import StrEnum


class GetContactResponse200DataNumbersItemType(StrEnum):
    FAX = "fax"
    PHONE = "phone"

    def __str__(self) -> str:
        return str(self.value)
