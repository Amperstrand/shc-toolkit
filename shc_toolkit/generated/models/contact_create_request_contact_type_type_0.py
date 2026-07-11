from enum import Enum


class ContactCreateRequestContactTypeType0(str, Enum):
    BILLING = "billing"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
