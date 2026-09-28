from enum import StrEnum


class ContactCreateResponseContactType(StrEnum):
    BILLING = "billing"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
