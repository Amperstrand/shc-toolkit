from enum import StrEnum


class ListContactsResponse200ItemsItemContactType(StrEnum):
    BILLING = "billing"
    OTHER = "other"
    PRIMARY = "primary"

    def __str__(self) -> str:
        return str(self.value)
