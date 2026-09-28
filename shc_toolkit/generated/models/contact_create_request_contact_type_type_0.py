from enum import StrEnum


class ContactCreateRequestContactTypeType0(StrEnum):
    BILLING = "billing"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
