from enum import StrEnum


class GetContactResponse200DataContactType(StrEnum):
    BILLING = "billing"
    OTHER = "other"
    PRIMARY = "primary"

    def __str__(self) -> str:
        return str(self.value)
