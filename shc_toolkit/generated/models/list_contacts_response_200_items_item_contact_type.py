from enum import Enum


class ListContactsResponse200ItemsItemContactType(str, Enum):
    BILLING = "billing"
    OTHER = "other"
    PRIMARY = "primary"

    def __str__(self) -> str:
        return str(self.value)
