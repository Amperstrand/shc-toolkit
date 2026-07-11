from enum import Enum


class ContactCreateResponseContactType(str, Enum):
    BILLING = "billing"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
